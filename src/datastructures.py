
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        if not member.get("id"):
            member["id"] = self._generateId()
        self._members.append(member)

    def delete_member(self, member_id):
        member_to_delete = None
        for member in self._members:
            if member["id"] == member_id:
                member_to_delete = member
                break
        if member_to_delete:
            self._members.remove(member_to_delete)
            return True
        return False

    def update_member(self, member_id, updated_member):
        for i, member in enumerate(self._members):
            if member["id"] == member_id:
                self._members[i] = {**member, **updated_member}
                self._members[i]["id"] = member_id  # Ensure the ID doesn't change
                return True
        return False

    def get_member(self, member_id):
        for member in self._members:
            if member["id"] == member_id:
                return member
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
