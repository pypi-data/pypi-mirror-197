# What's this?

A basic Python client for calling the TP-Link Omada controller API.

## Installation

```console
pip install tplink-omada-client
```

## Supported features

Only a subset of the controller's features are supported:
* Automatic Login/Re-login
* Basic controller information
* List sites
* Within site:
    * List Devices (APs, Gateways and Switches)
    * Basic device information
    * Get firmware information and initiating automatic updates
    * Port status and configuraton for Switches
    * Lan port configuration for Access Points

Tested with OC200 on Omada Controller Version 5.5.7 - 5.7.6. Other versions may not be fully compatible.

## Future

The available API surface is quite large. More of this could be exposed in the future.
There is an undocumented Websocket API which could potentially be used to get a stream of updates. However,
I'm not sure how fully featured this subscription channel is on the controller. It seems to be rarely used,
so probably doesn't include client connect/disconnect notifications.

## Contributing

There is a VS Code development container, which sets up all of the requirements for running the package.

## License

MIT Open Source license.
