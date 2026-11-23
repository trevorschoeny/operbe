# Adopting operbe

*Part of operbe. This guide covers how a project starts using the method and how it keeps up as the method changes.*

## A new project

1. Copy `templates/operbe.md` to the project's root. Set the version and name the UIs.
2. Create the two folders it names.
3. Work the first feature through the loop in `tandem.md`. Don't try to list everything up front. The lists grow as the features do.
4. Run `scripts/check.py <project root> --write`.
5. Make the check part of finishing work: a change isn't done until the check passes.

## A project that already exists

You don't need to stop and document everything.

1. Add `operbe.md` as above.
2. Make new work conform. Every new operation gets a record, and every new or changed piece of UI gets a behavior.
3. Write old work down when it is next touched. Whoever changes an existing screen or call adds its records then.
4. List what doesn't conform under "Known deviations" in `operbe.md`, for example "the phone UI calls two server routes that aren't operations yet". That list may only shrink.
5. Do one sweep for the easy part. Everything that already crosses the membrane is an operation whether or not it is written down, and listing the names is quick.

## Who owns what

The designer owns the behavior list. Anyone may propose a behavior or a change, and the designer decides.

Whoever builds the server owns the operation list. Each UI's builder owns that UI's coverage file.

One person may hold all three roles. They still matter, because they say whose word settles a disagreement.

## Working with agents

- Give a building agent one behavior record and the index. Don't give it the whole list.
- Have a different agent, or a person, check the result against the examples.
- An agent that finds a UI doing something off the list raises it. It doesn't add or remove it.
- Put anything that must hold every time in the check script or the project's own checks. Instructions are advice, and agents sometimes skip advice.

## Keeping up with the method

`operbe.md` records the version the project follows. The method's changelog (`CHANGELOG.md` in the operbe repository, github.com/trevorschoeny/operbe) says what changed in each version and what a project must do about it.

A rule in the method is experimental until it has worked in two projects. Experimental rules may change without a new major version.

## When the method doesn't fit

Record the deviation in `operbe.md` and carry on. If the same deviation shows up in a second project, the method is probably wrong, and it should be fixed at the source.
