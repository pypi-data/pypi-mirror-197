# ETH IAM Webservice

Manage users, groups and services of the ETH Identity and Access Management system (IAM)

## Synopsis

```
import ethz_iam_webservice
import getpass

password = getpass.getpass()

e = ethz_iam_webservice.login('admin4iam', password)

person = e.get_person('name@example.com')
person = e.get_person('some_username')
person = e.get_person(123456) # npid, the identifer of every person

person.usernames     # an array of dicts of usernames
person.data          # the whole response
person.firstname
person.familyname
person.email
# etc.

user = e.get_user('username')
person = user.get_person()
user.services        # returns an array of dicts of services

user.grant_service("LDAPS")
user.grant_service("Active Directory")
user.grant_service("WLAN_VPN")

user.revoke_service("LDAPS")
# etc.

user.delete()  # Method currently not allowed
```
