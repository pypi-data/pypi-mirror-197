===================
AFEX SSO FOR DJANGO
===================

|pypi| |build| |coverage|

# Documentation


# AFEX Simple SSO Specification (DRAFT)


## Server

The server is a Django website that holds all the user information and
authenticates users.

## Client

The client is a website that provides login via SSO using the **Server**.

## Key

A unique key identifying a **Client**. This key can be made public.

## Secret

A secret key shared between the **Server** and a single **Client**. This secret
should never be shared with anyone other than the **Server** and **Client** and
must not be transferred unencrypted.

Workflow

---
- User wants to log into a **Client** by clicking a "Login" button. The
  initially requested URL can be passed using the `next` GET parameter.
- The **Client**'s  code does a HTTP request to the **Server** to request a
  authentication token, this is called the **Request Token Request**.



