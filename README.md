# Firefox code review statistics

Analysis of Firefox code reviews using the [Phabricator] code review system.

## Setup

This project uses [Pipenv] to manage its dependencies.

To install the project dependencies:

```console
$ pipenv install
```

Before fetching any data you will need a Phabricator [API token] on Mozilla's 
Phabricator instance.  You may already have an API token in your home 
directory's `.arcrc` file:

```console
$ cat $HOME/.arcrc
```

If you do not have a token you can generate an [API token] from Mozilla's
Phabricator instance.

Add your Phabricator API token to a `.env` file in the project root:

```console
$ echo "CONDUIT_TOKEN=cli-myconduittoken12345" > .env
```

## Fetching the data

Enter into the `pipenv` shell before running any commands:

```console
$ pipenv shell
```

Run `make` in the project root to fetch the raw review data from the server
and process it for use.  This could take a while. ☕☕☕

```console
$ make
```

[Phabricator]: https://phabricator.services.mozilla.com
[pipenv]: https://pipenv.org
[API token]: https://phabricator.services.mozilla.com/conduit/
