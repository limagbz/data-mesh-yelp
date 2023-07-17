# Logical Architecture

This document aims to explain more deeply the logical architecture of this project. By logical architecture
understand:

> [...] An architecture that arranges the analytical data by domains. In this architecture, the domain’s
> interface to the rest of the organization not only includes the operational capabilities but also access
> to the analytical data that the domain serves.
> ― Zhamak Dehghani

1. [Diagram](#diagram)
1. [Domains](#domains)
1. [Operational Interfaces](#operational-interfaces)
1. [Entities](#entities)
1. [Analytical Interfaces](#operational-interfaces)

## Diagram

Below is the logical representation used by the project to model the domains, entities and
operational/analytical interfaces.

<p align="center">
<img src="_static/diagrams/logical-architecture.drawio.png" />
</p>

## Domains

* **User:** Domain responsible to manage information about the users and their interactions with another
users. This range from registration, friends, compliments and other user related capabilities.
* **Business:** Manage business information such as location, attributes, categories and related information.
Note that reviews, checkins and tips besides being very close to business they are in fact a relationship
between users and business, so they have their own domains to handle.
* **Evaluation:** Handle all types of evaluations from an user to a business (i.e. reviews and tips). This
is the only domain with multiple entities because of their similarities. According to Yelp, tips are
"a way to pass along some key information about a business [...] without writing a full review about your
experiences.". In fact, small reviews are converted automatically to tips in the platform.
* **Check-In:** Manage the user's check-ins on a business.

## Operational Interfaces

The operational interfaces described in the diagram are not an exhaustive list of capabilities for each
domain. They are rather a way of understand better which data each domain have control and to help develop the
products. Because of that some operational interfaces were omitted. For example, in a typical social network
besides the "Add a Friend" interface, others like "Accept Friend Request" and/or "Unfriend" are common. For a
simplified description and since the data will not reflect these kind of operations, these interfaces are not
presented.

<!-- TODO: See if this still applies in the future -->
> **Note** </br>
> Even if described here, some operational interfaces will not be simulated into the entities at first.
> However this can change as the project evolves.

## Entities

<!-- TODO: Add the path of the data generation script -->
> **Note** </br>
> You will notice that the entities described below have sightly modifications from the original data made
> available in the Yelp Dataset. These modifications were done to ensure a more faithful approach from a
> domain driven architecture. For example, on [`user.json`](https://www.yelp.com/dataset/documentation/main)
> file information such as`average_stars` or `review_count` were omitted from the User entity, this is
> because starts and reviews are available in the **evaluation** domain. All these changes will be reflected
> in the data used on the project. You can see the implementation details about this on the
> [data generation script]().

### User

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "User",
    "description": "A user for Yelp",
    "type": "object",
    "properties": {
        "user_id": {
            "description": "User 22-char unique identification",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "name": {
            "description": "User's Name",
            "type": "string",
        },
        "yelping_since": {
            "type": "string",
            "description": "User's creation date RFC4449 (ISO8601)",
            "format": "date"
        },
        "friends": {
            "type": "array",
            "description": "User's list of friends",
            "items": {
                "type": "string"
            }
        },
        "elite": {
            "type": "array",
            "description": "Years that the user was an Elite Member",
            "items": {
                "type": "integer"
            }
        },
    },
    "required": ["user_id", "name", "yelping_since", "friends", "elite"]
}
```

### Business

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Business",
    "description": "A business registered on Yelp",
    "type": "object",
    "properties": {
        "business_id": {
            "description": "22 character unique string business id",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "name": {
            "description": "Business' Name",
            "type": "string",
        },
        "address": {
            "type": "string",
            "description": "Full address of the business",
        },
        "city": {
            "type": "string",
            "description": "City name",
        },
        "state": {
            "type": "string",
            "description": "2 character state code, if applicable",
            "minLength": 2,
            "maxLength": 2,
        },
        "postal_code": {
            "type": "string",
            "description": "Postal Code",
        },
        "latitude": {
            "type": "number",
            "description": "Latitude",
        },
        "longitude": {
            "type": "number",
            "description": "Latitude",
        },
        "is_open": {
            "type": "boolean",
            "description": "0 or 1 for closed or open, respectively",
        },
        "attributes": {
            "type": "object",
            "description": "business attributes to values",
        },
        "categories": {
            "type": "array",
            "description": "business categories",
            "items": {
                "type": "string"
            }
        },
        "hours": {
            "type": "object",
            "description": " day to value hours, hours are using a 24hr clock (e.g. 10:00-21:00)",
            "properties": {
                "Monday": {"type": "string"},
                "Tuesday": {"type": "string"},
                "Wednesday": {"type": "string"},
                "Thursday": {"type": "string"},
                "Friday": {"type": "string"},
                "Saturday": {"type": "string"},
                "Sunday": {"type": "string"}
            },
            "required": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        }

    },
    "required": [
        "business_id", "name", "address", "city", "state", "postal_code", "latitude", "longitude",
        "is_open", "attributes", "categories", "hours"
    ]
}
```

### Reviews

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Reviews",
    "description": "A review on Yelp",
    "type": "object",
    "properties": {
        "review_id": {
            "description": "22 character unique string review id",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "business_id": {
            "description": "22 character unique string id identifying the reviewed business",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "user_id": {
            "description": "User 22-char unique string id identifying the user who wrote the review",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "stars": {
            "type": "integer",
            "description": "Star rating",
            "minimum": 0,
            "maximum": 5,
        },
        "date": {
            "type": "string",
            "description": "Review's creation date RFC4449 (ISO8601)",
            "format": "date"
        },
        "text": {
            "type": "string",
            "description": "Review text",
        },
        "useful": {
            "type": "integer",
            "description": "Number of useful votes received",
            "minimum": 0,
        },
        "funny": {
            "type": "integer",
            "description": "Number of funny votes received",
            "minimum": 0,
        },
        "cool": {
            "type": "integer",
            "description": "Number of cool votes received",
            "minimum": 0,
        },
    },
    "required": ["review_id", "business_id", "user_id", "stars", "date", "text", "useful", "funny", "cool"]
}
```

### Tips

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Tip",
    "description": "Tips written by an user to a business",
    "type": "object",
    "properties": {
        "business_id": {
            "description": "22 character unique string id identifying the business",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "user_id": {
            "description": "User 22-char unique string id identifying the user who wrote the Tip",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "date": {
            "type": "string",
            "description": "Tips' creation date RFC4449 (ISO8601)",
            "format": "date"
        },
        "text": {
            "type": "string",
            "description": "Tip text",
        },
        "compliment_count": {
            "type": "integer",
            "description": "How many compliments the tip has",
            "minimum": 0,
        },
    },
    "required": ["business_id", "user_id", "date", "text", "compliment_count"]
}
```

### Checkin

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Check-in",
    "description": "Checkins on a business",
    "type": "object",
    "properties": {
        "business_id": {
            "description": "22 character unique string id identifying the business",
            "type": "string",
            "minLength": 22,
            "maxLength": 22,
        },
        "checkins": {
            "type": "array",
            "description": "Check-ins with user and date",
            "items": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Review's creation date RFC4449 (ISO8601)",
                        "format": "date"
                    },
                    "user_id": {
                        "description": "User 22-char unique string id identifying the user",
                        "type": "string",
                        "minLength": 22,
                        "maxLength": 22,
                    },
                }
            }
        },
    },
    "required": ["business_id", "checkins"]
}
```

## Analytical Interfaces (a.k.a Data Products)

<!-- TODO: Add the path to the products folder -->
For more information about the Analytical interfaces described in the diagram. Refer to their own
documentation on [products folder]()
