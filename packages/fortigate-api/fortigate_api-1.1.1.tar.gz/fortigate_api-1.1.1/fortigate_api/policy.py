"""Policy Object"""

from requests import Response

from fortigate_api import str_
from fortigate_api.base import Base
from fortigate_api.extended_filters import wrapp_efilters
from fortigate_api.types_ import DAny
from fortigate_api.types_ import LDAny, StrInt


class Policy(Base):
    """Policy Object"""

    def __init__(self, fgt):
        super().__init__(fgt=fgt, url_obj="api/v2/cmdb/firewall/policy/", uid_key="policyid")

    # noinspection PyIncorrectDocstring
    @wrapp_efilters
    def get(self, **kwargs) -> LDAny:
        """Gets fortigate-objects, all or filtered by some of params.
        Need to use only one of params
        :param int uid: Filters fortigate-object by identifier. Used to get a single object
        :param list filter: Filters fortigate-objects by one or multiple conditions: equals "==",
            not equals "!=", contains "=@". Used to get multiple objects
        :param str efilter: Extended filter: "srcaddr", "dstaddr" by condition: equals "==",
            not equals "!=",  supernets ">=", subnets "<="
        :return: *List[dict_]* List of the fortigate-objects
        """
        return super().get(**kwargs)

    def move(self, uid: StrInt, position: str, neighbor: StrInt) -> Response:
        """Move policy to before/after other neighbor-policy
        :param uid: Identifier of policy being moved
        :param position: "before" or "after" neighbor
        :param neighbor: Policy will be moved near to this neighbor-policy
        :return: Session response
            *<Response [200]>* Policy successfully moved
            *<Response [500]>* Policy has not been moved
        """
        kwargs = dict(action="move", username=self.fgt.username, secretkey=self.fgt.password)
        kwargs[position] = neighbor
        url = f"{self.url_}{uid}"
        url = str_.make_url(url, **kwargs)
        return self.fgt.put(url=url, data={})

    def update(self, data: DAny, uid: StrInt = "") -> Response:
        """Updates policy-object in the Fortigate
        :param data: Data of the policy-object
        :param uid:  Policyid of the policy-object,
            taken from the `uid` parameter or from data["policyid"]
        :return: Session response
            *<Response [200]>* Object successfully updated
            *<Response [404]>* Object has not been updated
        """
        if not uid:
            uid = data.get("policyid") or ""
            if not uid:
                raise ValueError(f"absent {uid=} and data[\"policyid\"]")
        return self._update(uid=uid, data=data)
