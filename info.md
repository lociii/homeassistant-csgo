# CS:GO game state integration for Home Assistant

This integration makes Counter-Strike: Global Offensive game state changes available in Home Assistant.

## Setup - Home Assistant

Go to the integrations (Configuration -> Integrations) page and add the "CS:GO game state listener" integration.

During the setup process, the integration will create a webhook and show the uri parameter for the CS:GO configuration. 
Make sure to copy this code to your clipboard.

## Setup - CS:GO

CS:GO has an integrated game state reporting engine that we will use no update Home Assistant.

The configuration will be added to your CS:GO config directory.
[How to find my config directory](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration#Locating_CS:GO_Install_Directory)

Open that directory and add a file called **gamestate_integration_homeassistant.cfg**.

Add the following content and replace the "uri" with the one copied during the integration setup:

```
"HomeAssistant Integration v.1"
{
 "uri" "https://hooks.nabu.casa/xyz"
 "timeout" "5.0"
 "buffer" "0.1"
 "throttle" "0.5"
 "heartbeat" "15.0"
 "data"
 {
   "round" "1" // round phase, bomb state and round winner
 }
}
```

## Events

When everything is set up properly, the integration will start firing events as game state changes happen.

The following events are currently supported:

### csgo_round_freeze

Freeze time before a round started

### csgo_round_started

New round started

### csgo_round_ended

Round ended

### csgo_bomb_planted

The bomb was planted

### csgo_bomb_defused

The bomb was defused

### csgo_bomb_exploded

The bomb exploded

### csgo_game_stopped

The game has been closed

## Automations

Use these events to trigger automations that control your lights, sounds, fireworks, etc.

Have fun!

## Example usages

* [Control lights](https://www.youtube.com/watch?v=kEM54QmAMlw)
* [Start real fire when bomb explodes](https://automatedhome.party/2020/03/28/summoning-actual-fire-or-other-automations-when-the-bomb-goes-off-in-csgo-via-home-assistant/)
