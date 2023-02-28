import pymysql
import networkx as nx
import matplotlib.pyplot as plt


class DB:
    def __init__(self, user, password, database, host="localhost", charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor):
        # Connect to the database
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          database=database,
                                          charset=charset,
                                          cursorclass=cursorclass)

    def primary_select(self, table: str, columns: list, keys: list, verbose=False):
        if len(columns) != len(keys):
            raise Exception("the length of column and keys must be same")
        sql = "select * from `%s` where `%s` = \"%s\"" % (table, columns[0], keys[0])
        if len(columns) > 1:
            for i in zip(columns[1:], keys[1:]):
                sql += " and `%s`=\"%s\"" % i
        if verbose:
            print(sql)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res

    def check_existence(self, table: str, columns: list, keys: list, verbose=False) -> bool:
        res = self.primary_select(table, columns, keys, verbose)
        if len(res) == 0:
            return False
        else:
            return True

    def current_id(self, table, id):
        sql = "SELECT `%s` FROM `%s` ORDER BY `%s` DESC LIMIT 1" % (id, table, id)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            if len(res) == 0:
                return 0
            else:
                return res[0][id]

    def update_by_info_dict(self, info_dict):
        with self.connection.cursor() as cursor:
            # cursor.
            # update paper entities
            if self.check_existence("Paper", ["title"], [info_dict["title"]]) == False:
                sql = "INSERT INTO Paper(title, DOI, date, url) VALUE (\"%s\", \"%s\", \"%s\", \"%s\")" % (
                    info_dict["title"], info_dict["doi"], info_dict["date"], info_dict["url"])
                cursor.execute(sql)
                paper_id = self.current_id("Paper", "id")
                # update author and location entities
                for i in info_dict["authors"]:
                    if self.check_existence("Author", ["first_name", "second_name"],
                                            [i["name"]["given"], i["name"]["family"]]) == False:
                        orcid = "empty"
                        if i["ORCID"] != None and i["ORCID_trust"] == True:
                            if isinstance(i["ORCID"], list):
                                orcid = i["ORCID"][0]
                            else:
                                orcid = i["ORCID"]
                        sql = "INSERT INTO Author(first_name, second_name, ORCID) VALUE (\"%s\", \"%s\", \"%s\")" % (
                            i["name"]["given"], i["name"]["family"], orcid)
                        cursor.execute(sql)
                        author_id = self.current_id("Author", "id")
                        sql = "INSERT INTO Authorship(author_id, paper_id) VALUE (\"%d\", \"%d\")" % (
                            author_id, paper_id)
                        cursor.execute(sql)
                        for j in i["location"]:
                            if self.check_existence("Location", ["name"], [j]) == False:
                                sql = "INSERT INTO Location(name) VALUE (\"%s\")" % j
                                cursor.execute(sql)
                                location_id = self.current_id("Location", "id")
                                sql = "INSERT INTO Locate(author_id, location_id) VALUE (\"%d\",\"%d\")" % (
                                    author_id, location_id)
                                cursor.execute(sql)
                            else:
                                location_id = self.primary_select("Location", ["name"], [j])[0]["id"]
                                sql = "INSERT INTO Locate(author_id, location_id) VALUE (\"%d\",\"%d\")" % (
                                    author_id, location_id)
                                cursor.execute(sql)
                    else:
                        author_id = self.primary_select("Author", ["first_name", "second_name"],
                                                        [i["name"]["given"], i["name"]["family"]])[0]["id"]
                        sql = "INSERT INTO Authorship(author_id, paper_id) VALUE (\"%d\", \"%d\")" % (
                            author_id, paper_id)
                        cursor.execute(sql)
                # update outer reference entities
                for i in info_dict["references"]:
                    if self.check_existence("Paper", ["title"], [
                        i["title"]]) == False:  # this reference is not in previous Paper, then update outer ref
                        sql = "INSERT INTO Outer_reference(title, type) VALUE (\"%s\", \"%s\")" % (
                            i["title"], i["type"])
                        cursor.execute(sql)
                        outer_ref_id = self.current_id("Outer_reference", "id")
                        sql = "INSERT INTO OR_cite(paper_id, Outer_reference_id) VALUE (\"%d\", \"%d\")" % (
                            paper_id, outer_ref_id)
                        cursor.execute(sql)
                    else:  # this reference is in previous Paper
                        inner_ref_id = self.primary_select("Paper", ["title"], [i["title"]])[0]["id"]
                        sql = "INSERT INTO IR_cite(paper_id, cited_paper_id) VALUE (\"%d\", \"%d\")" % (
                            paper_id, inner_ref_id)
                        cursor.execute(sql)
            else:
                pass  # paper already exists, do nothing

        self.connection.commit()

    # return a list of Paper_id
    def find_paper(self, title: str, *doi) -> list[dict[str, int]]:
        with self.connection.cursor() as cursor:
            sql = ""
            if len(doi) != 0:
                sql = "select id from Paper where DOI = %s"
                cursor.execute(sql, doi)
            else:
                sql = "select id from Paper where title = %s"
                cursor.execute(sql, title)
            paper = cursor.fetchall()
            try:
                if len(paper) == 0:
                    if len(doi) != 0:
                        raise Exception('Cannot find existing paper by this DOI: \'{}\''.format(doi[0]))
                    else:
                        raise Exception('Cannot find existing paper by this title: \'{}\''.format(title))
                if len(paper) >= 2:
                    raise Exception('Found more than 1 paper with the same name:\'{}\''.format(title))
            except Exception as e:
                print(e)
                return
            return paper

    # return a list of Author's id
    def find_author(self, first_name: str, second_name: str, *orcid) -> list[dict[str, int]]:
        with self.connection.cursor() as cursor:
            if len(orcid) != 0:
                sql = "select id from Author where ORCID = %s"
                cursor.execute(sql, orcid)
            else:
                sql = "select id from Author where first_name = %s and second_name = %s"
                cursor.execute(sql, (first_name, second_name))
            author = cursor.fetchall()
            try:
                if len(author) == 0:
                    if len(orcid) != 0:
                        raise Exception('Cannot find existing paper by this DOI: \'{}\''.format(orcid[0]))
                    else:
                        raise Exception(
                            'Cannot find existing paper by this title: \'{} {}\''.format(first_name, second_name))
                if len(author) >= 2:
                    raise Exception(
                        'Found more than 1 paper with the same name:\'{} {}\''.format(first_name, second_name))
            except Exception as e:
                print(e)
                return
            return author

    # return a list of Outer_reference_id
    def find_outer_reference(self, title: str):
        with self.connection.cursor() as cursor:
            sql = "select id from Outer_reference where Title = %s"
            cursor.execute(sql, title)
            result = cursor.fetchall()
            return result

    # return paper info
    def inner_paper_info(self, papers: list[dict[str, int]]) -> dict[str,]:
        with self.connection.cursor() as cursor:
            result = []
            for paper in papers:
                for value in paper.values():
                    sql = "select * from Paper where id = %s"
                    cursor.execute(sql, value)
                    result.extend(cursor.fetchall())
            return result

    # Return a list of papers' id which were written by the input author with name or ORCID.
    def authorship_relation(self, first_name: str, second_name: str, *orcid):
        author = self.find_author(first_name, second_name, *orcid)
        if author is None:
            return
        with self.connection.cursor() as cursor:
            sql = "select paper_id from Authorship where Author_id = %s order by Paper_id"
            cursor.execute(sql, author[0]['id'])
            papers: list[dict[str, int]] = cursor.fetchall()
            return papers

    # RETURN The full info of papers written by the author
    def authorship_relation_full_info(self, first_name: str, second_name: str, *orcid):
        papers = self.authorship_relation(first_name, second_name, *orcid)
        return self.inner_paper_info(papers)

    # Return a list of paper id (exist in database) that cited by the input paper.
    # if title and doi are both provided, will only search by doi
    # direction = 0 means to find the reference of the input paper
    # direction = 1 means to find papers which are citing the input paper
    def ir_cite_relation(self, title: str, direction, *doi) -> list[dict[str, int]]:
        paper = self.find_paper(title, *doi)
        if paper is None:
            return
        with self.connection.cursor() as cursor:
            if direction == 0:
                sql = "select cited_paper_id from IR_cite where paper_id = %s order by cited_paper_id"
            else:
                sql = "select paper_id from IR_cite where cited_paper_id = %s order by paper_id"
            cursor.execute(sql, paper[0]['id'])
            papers = cursor.fetchall()
            return papers

    # return the full info of references of the input paper
    def ir_cite_relation_full_info(self, title: str, direction, *doi):
        papers = self.ir_cite_relation(title, direction, *doi)
        result = self.inner_paper_info(papers)
        return result

    # return the id of outer references
    def outer_ref_info(self, outer_refs: list[dict[str, int]]) -> list[dict[str,]]:
        with self.connection.cursor() as cursor:
            result = []
            for outer_ref in outer_refs:
                for value in outer_ref.values():
                    sql = "select * from Outer_reference where id = %s"
                    cursor.execute(sql, value)
                    result.extend(cursor.fetchall())
            return result

    # Return a list of outer references id of the input paper.
    def or_cite_relation(self, title: str, *doi) -> list[dict[str, int]]:
        paper = self.find_paper(title, *doi)
        if paper is None:
            return
        with self.connection.cursor() as cursor:
            sql = "select Outer_reference_id from OR_cite where paper_id = %s order by Outer_reference_id"
            cursor.execute(sql, paper[0]['id'])
            outer_references = cursor.fetchall()
            return outer_references

    def or_cite_relation_full_info(self, title: str, *doi) -> list[dict[str,]]:
        outer_references = self.or_cite_relation(title, *doi)
        result = self.outer_ref_info(outer_references)
        return result

    # Return a list of paper(s) that the two input authors' name/ORCID have in common.
    # If such paper does not exist, return an empty list.
    def check_cooperation(self, author0_first_name, author0_second_name, author1_first_name, author1_second_name,
                          *orcid):
        orcid0 = orcid1 = ()
        if len(orcid) == 2:
            orcid0 = orcid[:1]
            orcid1 = orcid[1:]
        elif len(orcid) == 1:
            orcid0 = orcid[:1]
        paper0 = self.authorship_relation(author0_first_name, author0_second_name, *orcid0)
        paper1 = self.authorship_relation(author1_first_name, author1_second_name, *orcid1)
        if paper0 is None or paper1 is None:
            return
        set1 = {frozenset(d.items()) for d in paper0}
        set2 = {frozenset(d.items()) for d in paper1}
        intersection = [dict(s) for s in (set1 & set2)]
        return intersection

    # Return a boolean that indicate whether if the input paper1 is cited by paper0.
    def check_ir_cite(self, title0, title1, *doi):
        doi0 = doi1 = ()
        if len(doi) == 2:
            doi0 = doi[:1]
            doi1 = doi[1:]
        elif len(doi) == 1:
            doi0 = doi[:1]
        paper0 = self.find_paper(title0, *doi0)
        paper1 = self.find_paper(title1, *doi1)
        if paper0 is None or paper1 is None:
            return
        with self.connection.cursor() as cursor:
            sql = "select Cited_Paper_id from IR_cite where paper_id = %s order by Cited_Paper_id"
            cursor.execute(sql, paper0[0]['id'])
            cited_papers = cursor.fetchall()
            for cited_paper in cited_papers:
                if cited_paper['Cited_Paper_id'] == paper1[0]['id']:
                    return True
            return False

    # Return a boolean that indicate whether if the input outer reference have been cited in the input paper.
    def check_or_cite(self, title, or_title, *doi):
        outer_refs = self.or_cite_relation(title, *doi)
        if outer_refs is None:
            return False
        for outer_ref in outer_refs:
            if outer_ref['title'].lower() == or_title.lower():
                return True
        return False

    def find_author_location(self, name, *orcid):
        author = self.find_author()

    # return true if paper_id is in record, else return false and put the paper_id into record
    def if_in_record(self, paper_id: int) -> bool:
        if paper_id in self.record:
            return True
        else:
            self.record.append(paper_id)
            return False

    # return papers' id which are related with the input paper
    def find_relation_by_paper(self, depth_limit, depth_now, papers: list[dict[str, int]], result: list[
        tuple[int, int]]):
        if depth_now > depth_limit or len(papers) == 0:
            return
        with self.connection.cursor() as cursor:
            references = citings = []
            for paper in papers:
                for paper_id in paper.values():
                    if self.if_in_record(paper_id):
                        continue
                    # find reference
                    sql = "select cited_paper_id from IR_cite where paper_id = %s"
                    cursor.execute(sql, paper_id)
                    references = cursor.fetchall()
                    for reference in references:
                        for reference_id in reference.values():
                            result.append((paper_id, reference_id))
                    # find papers citing this paper
                    sql = "select paper_id from IR_cite where cited_paper_id = %s"
                    cursor.execute(sql, paper_id)
                    citings = cursor.fetchall()
                    for citing in citings:
                        for citing_id in citing.values():
                            result.append((citing_id, paper_id))
                self.find_relation_by_paper(depth_limit, depth_now + 1, references, result)
                self.find_relation_by_paper(depth_limit, depth_now + 1, citings, result)
            return

    # this list is to assist the connection algorithm,
    # it will record the paper_id that has been processed
    record = []

    # will show the connection of the input paper
    def show_inner_connection(self, title, depth, *doi):
        # the paper itself
        paper = self.find_paper(title, *doi)
        result = []
        self.record = []
        self.find_relation_by_paper(depth, 1, paper, result)
        print(result)
        G = nx.DiGraph(result)
        pos = nx.planar_layout(G)
        nx.draw(G, with_labels=True, pos=pos)
        plt.show()


if __name__ == "__main__":
    db = DB("root", "18170620626Xad", "psd")
    # print(db.authorship_relation_full_info('Anton', 'xia', '0000-0002-9367-2206'))
    # print(db.check_or_cite('sas', 'kill bill', '1234567'))
    # print(db.check_ir_cite('secon', '', '123', '1234567'))
    # print(db.check_cooperation('Anton', 'xiao', 'piche', 'zhao', ))
    # print(db.or_cite_relation('second\'paper', '10.1145/3491418.3530773')
    # print(db.ir_cite_relation('secon', 0,'10.1145/3491418.3530773'))
    print(db.show_inner_connection('secon', 5, '10.1145/3491418.3530773'))
