# PyClient

Python Client for retrieving Bioto sensor data

## Goals

### Session management

- [x] create session via device login to get a valid access token

### Retrieving sensor data

- [x] find a garden
- [x] subscribe to that garden
- [x] see subscribtion state for that garden (pending/approved/declined)
- [x] get an overview of your gardens
- [x] retrieve sensor data from garden devices

## Getting started

There are two ways of installing this client. The first one using pip:

```bash
% pip install --user bioto-client
```

The second option is useful when developing the client. Git clone the project
and use `make` for installation. This will setup a
[virtual python environment][3] managed via [`poetry`][4].

```bash
% make install
% poetry shell
```

## How to use

> **Tip** Use `bioto-client --help` to see other available commands

### Start a user session

A user session is valid for 24h. When expired you're requested to create a new
session. This can be done as follows:

```bash

# Call the client with the `user` command to assert a valid session
% bioto-client user

Loading session

Not logged in, please take the following steps:

1. On your computer or mobile device navigate to: https://biotoco.eu.auth0.com/activate?user_code=NEWT-OKEN
2. Enter the following code:  NEWT-OKEN

Succesfully logged in.

Bioto CLI client: 1.2.3
Environment: prod
Session token ***5OFd09w
```

### Find a garden

Gardens can be found by name, the command to do this is:

```bash
% bioto-client search-garden {name}
```

### Subscribe to a garden

To gain access to the data of this garden you need to subscribe to this garden
using its `ID`:

```bash
% bioto-client subscribe-garden {garden_id}
```

This will create a subscription request which only the mainter(s) can approve.
To check the state of your subscription see:

```bash
% bioto-client subscriptions
```

### Read device data

Reading a device is done by `device ID`, these can be found via the garden
command. Note that a garden might contain multiple devices.

To get the latest hourly readings for the last 24h issue the following command:

```bash
% bioto-client device {device_id}
```

To get these readings for a sepecific date apply a date option. The following
formats are allowed: [%Y-%m-%d | %Y-%m-%dT%H:%M:%S | %H:%M:%S]:

```bash
% bioto-client device {device_id} --date={date}
```

And to limit or increase the number of hours returned add the hours option:

```bash
% bioto-client device {device_id} --hours={hours_limit}
```

## Improve the client

If you want to improve the client or add something which you think is missing to
the project you can either [open an issue][1] or develop the feature yourself
and open [a pull request with your changes][2].

To get started clone this project and create a branch. Now fix the bug or create
the feature you want and write some tests for it to prove it works. This can be
done by executing:

```bash
% make check
```

> **Note** This will run both tests and linters, use `make test` when you're in
`red - green - refactor` mode

When the checks are all passing, please open a [PR][2]

[1]: https://github.com/wearebioto/PyClient/issues
[2]: https://github.com/wearebioto/PyClient/pulls
[3]: https://docs.python.org/3/library/venv.html
[4]: https://python-poetry.org/docs/
