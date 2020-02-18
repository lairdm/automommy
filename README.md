# Automommy

I needed a method for my wife to quickly and hands free play tv shows for our elder daughter while the other was napping.

As well, I can see it being useful as they grow to limit what shows they can watch on their own. Setting up a small upset of shows they're allowed to launch.

This repo is a set of webhooks and lambda functions that link together an Alexa skill to playing media on our tv.

Alexa -> Lambda -> SNS -> Django (home file server) -> Roku (Plex & Youtube)

It has zero resiliency and error checking, more of a fire and forget, either it works or doesn't. Partially because it's a quick little project, partially because the Alexa skill has no async feedback mechanism because it's not tied to a user login.

But if you find any of the pieces useful to learn for your own project, have at it.

# Technologies in use

- Lambda (Python 3.x)
- DynamoDB (so the Lambda knows if we have a show before sending the message, no async feedback)
- SNS (send messages home)
- Django (receive webhooks)
- Roku Python API and ECP (External Control Protocol)
- Plex Python API
- Postgres (store where each show lives, what the last shown episode was)

# TODO

## Web interface

I need to be able to launch shows without saying anything, in case one daughter is sleeping

## TV Control

In theory I can turn the LG tv on, and set the volume and input via RS232 interface. I haven't had a chance to get that working yet. I'd probably hook it up to a Raspberry Pi sitting behind the TV.

It could even set a timer for the show length and turn the TV back off. We can ask Plex if something is playing, but we can't tell if a Youtube video is still playing in the Roku app.

# More commands

"Play a half hour show"

"Play a movie"

etc.

## Infrastructure as code

Most AWS services were setup using the web interfaces. I dislike this. I need to use Serverless and other frameworks to auto-deploy the system so the settings can all be in a VCS.

## Multi-TV support

Maybe in the future the kids will need to say, "play x in the rec room"

## Launch Netflix shows

Is there a way to inject shows in to the launching of the Netflix app on a Roku? That's how the Youtube app works. Or very careful use of the `literals` search function via the Roku ECP?

## Proper modularization

The code is a mess. But it works. And it's not in production outside our household. ¯\_(ツ)_/¯

# Next Steps

Let's be honest, probably none. Once it works I'll probably leave it alone until it breaks or I need a new feature.
