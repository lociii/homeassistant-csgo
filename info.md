
# Examples of automation that play nice with Yeelight 
Automations:
```
- id: cs2_round_freeze
  alias: CS2 – Freezetime starts
  trigger:
  - platform: event
    event_type: csgo_round_freeze
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_freezetime
- id: cs2_round_started
  alias: CS2 – Round starts
  trigger:
  - platform: event
    event_type: csgo_round_started
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_begin_end
- id: cs2_bomb_planted
  alias: CS2 – Bomb planted
  trigger:
  - platform: event
    event_type: csgo_bomb_planted
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_bomb_planted
- id: cs2_bomb_exploded
  alias: CS2 – Bomb exploded
  trigger:
  - platform: event
    event_type: csgo_bomb_exploded
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_bomb_exploded
- id: cs2_bomb_defused
  alias: CS2 – Bomb defused
  trigger:
  - platform: event
    event_type: csgo_bomb_defused
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_bomb_defused
- id: cs2_game_stopped
  alias: CS2 – Game stopped
  trigger:
  - platform: event
    event_type: csgo_game_stopped
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_game_stopped
- id: cs2_player_flashed
  alias: CS2 – Player flashed
  trigger:
  - platform: event
    event_type: csgo_player_flashed
  condition:
  - condition: state
    entity_id: light.lightname
    state: 'on'
  action:
  - service: script.turn_on
    target:
      entity_id: script.csgo_flashloop
```

Scripts:
```
csgo_freezetime:
  alias: CS2 – Freezetime
  sequence:
    - service: yeelight.set_mode          # ensure any flow stops
      data:
        entity_id: light.lightname
        mode: normal
    - service: light.turn_on
      target:
        entity_id: light.lightname
      data:
        rgb_color: [83, 52, 235]
        transition: 0.5

csgo_begin_end:
  alias: CS2 – Round start / end
  sequence:
    - service: yeelight.set_mode
      data:
        entity_id: light.lightname
        mode: normal
    - service: light.turn_on
      target:
        entity_id: light.lightname
      data:
        rgb_color: [255, 244, 229]        # neutral warm-white
        transition: 1

csgo_bomb_planted:
  alias: CS2 – Bomb planted
  sequence:
    - service: yeelight.set_mode          # stop any previous flow
      data:
        entity_id: light.lightname
        mode: normal
    - service: light.turn_on              # orange hint
      target:
        entity_id: light.lightname
      data:
        rgb_color: [255, 190, 0]
        transition: 0.5
    - delay: "1"
    - service: script.turn_on             # start infinite flash
      target:
        entity_id: script.csgo_flashloop

csgo_bomb_defused:
  alias: CS2 – Bomb defused
  sequence:
    - service: yeelight.set_mode
      data:
        entity_id: light.lightname
        mode: normal
    - service: light.turn_on
      target:
        entity_id: light.lightname
      data:
        rgb_color: [0, 255, 0]
        transition: 0.5

csgo_bomb_exploded:
  alias: CS2 – Bomb exploded
  sequence:
    - service: yeelight.set_mode
      data:
        entity_id: light.lightname
        mode: normal
    - service: light.turn_on
      target:
        entity_id: light.lightname
      data:
        rgb_color: [255, 0, 0]
        transition: 0.5

csgo_game_stopped:
  alias: CS2 – Game stopped
  sequence:
    - service: yeelight.set_mode
      data:
        entity_id: light.lightname
        mode: normal             # restore normal mode
    - service: yeelight.set_mode # ensure “normal” scene
      data:
        entity_id: light.lightname
        mode: normal

# -------------  Infinite white strobe (one API call) -------------
csgo_flashloop:
  alias: CS2 – Flash loop (infinite)
  mode: restart
  sequence:
    # 1. Make absolutely sure any old flow is gone
    - service: yeelight.set_mode
      data:
        entity_id: light.lightname
        mode: normal
    - delay: 0.2          # tiny pause so the bulb is ready

    # 2. Start a brand-new infinite strobe handled by the bulb itself
    - service: yeelight.start_flow
      data:
        entity_id: light.lightname
        count: 0           # 0 = loop forever
        action: stay       # stay in last frame when we later stop it
        transitions:
          # 0.4 s bright white …
          - RGBTransition: [255, 255, 255, 400, 100]
          # … then 0.4 s fully off (sleep = LEDs off)
          - SleepTransition: 400
```

***This example was using a Yeelight integration, so some changes may be needed to fit to other smart lights.. ***

# CS:GO game state integration for Home Assistant

This integration makes Counter-Strike: Global Offensive game state changes available in Home Assistant.

## Setup - Home Assistant

First make sure that your instance is reachable via URL. Go to `Configuration > Settings > General` and set `Internal URL` and `External URL`.

Then go to `Configuration > Devices and Services > Integrations`. Press the `Add integration` button and add the "CS:GO game state listener" integration.

During the setup process, the integration will create a webhook and show the URI parameter for the CS:GO configuration.
Make sure to copy this code to your clipboard.

## Setup - CS:GO

CS:GO has an [integrated game state reporting engine](https://www.reddit.com/r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth/) that we will use no update Home Assistant.

The configuration will be added to your CS:GO config directory.
[How to find my config directory](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration#Locating_CS:GO_Install_Directory)

Open that directory and add a file called **gamestate_integration_homeassistant.cfg**.

Add the following content and replace the "uri" with the one copied during the integration setup:

```
"HomeAssistant Integration v1.2.0"
{
 "uri" "https://hooks.nabu.casa/xyz"
 "timeout" "5.0"
 "buffer" "0.1"
 "throttle" "0.5"
 "heartbeat" "15.0"
 "data"
 {
   "round"          "1" // round phase, bomb state and round winner
   "player_state"   "1" // player state (used for health)
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

### csgo_health_low

Player health is between 11 and 30

### csgo_health_critical

Player health is 10 or lower

### csgo_player_flashed

Player flashed intensity as integer from 0 (not flashed) to 255 (fully flashed)

### csgo_round_win_ct

CT team won the round

### csgo_round_win_t

T team won the round

## Automations

Use these events to trigger automations that control your lights, sounds, fireworks, etc.

Have fun!

## Example usages

- [Control lights](https://www.youtube.com/watch?v=kEM54QmAMlw) ([Community thread explaing the config used in the video](https://community.home-assistant.io/t/counter-strike-global-offensive-game-state-integration/175505))
- [Start real fire when bomb explodes](https://automatedhome.party/2020/03/28/summoning-actual-fire-or-other-automations-when-the-bomb-goes-off-in-csgo-via-home-assistant/)
