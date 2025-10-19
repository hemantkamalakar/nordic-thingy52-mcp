# Nordic Thingy:52 MCP Server - Prompt Guide

**Advanced automation and usage examples for the 25 MCP tools**

This guide showcases the full capabilities of the Nordic Thingy:52 MCP Server through real-world automation scenarios and natural language prompts.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Environmental Monitoring](#environmental-monitoring)
- [Motion & Orientation](#motion--orientation)
- [Smart Alerts & Notifications](#smart-alerts--notifications)
- [Multi-Sensor Workflows](#multi-sensor-workflows)
- [Advanced Automation](#advanced-automation)
- [Professional Applications](#professional-applications)
- [Creative Use Cases](#creative-use-cases)

## Quick Reference

### Basic Commands
```
"Scan for nearby Thingy devices"
"Connect to my Thingy"
"What's my device status?"
"Read all sensors"
"Set LED to blue"
"Play sound 3"
"Turn everything off"
```

### Get Help
```
"Show me all available sensors"
"What MCP tools are available?"
"Give me examples of what I can do with the Thingy"
"How do I monitor air quality?"
```

## Environmental Monitoring

### Temperature Monitoring

**Basic Reading**
```
"What's the current temperature?"
"Is it warmer than 25°C?"
```

**Temperature Alerts**
```
"Monitor the temperature. If it goes above 28°C, set LED to red and play sound 5.
If it drops below 18°C, set LED to blue and play sound 2."
```

**Temperature Logging**
```
"Read the temperature every 5 minutes for the next hour.
Show me a summary with min, max, and average values."
```

### Humidity Tracking

**Comfort Monitoring**
```
"Check if humidity is in the comfortable range (40-60%).
If it's too dry (<40%), show yellow LED.
If it's too humid (>60%), show orange LED.
If it's comfortable, show green LED."
```

**Mold Prevention**
```
"Monitor humidity in my bathroom. If it exceeds 70% for more than 5 minutes,
alert me with red LED breathe and sound 8. This could indicate mold risk."
```

### Air Quality Monitoring

**CO2 Alerts with Multi-Level Response**
```
"Create a comprehensive CO2 monitoring system:

Level 1 (< 800 ppm): Excellent air quality
- Green LED constant
- No alerts

Level 2 (800-1000 ppm): Good air quality
- Blue LED constant
- No action needed

Level 3 (1000-1500 ppm): Moderate - ventilation recommended
- Yellow LED breathe (1 second interval)
- Play sound 2
- Message: 'Consider opening a window'

Level 4 (1500-2000 ppm): Poor - ventilation needed
- Orange LED breathe (500ms interval)
- Play sound 5
- Message: 'Open windows immediately'

Level 5 (> 2000 ppm): Very poor - urgent action
- Red LED breathe (250ms interval)
- Play sound 8 every minute
- Message: 'URGENT: Severe air quality - evacuate if necessary'

Check every 30 seconds and update status."
```

**Combined Air Quality**
```
"Monitor both CO2 and TVOC levels.
If CO2 > 1200 ppm OR TVOC > 500 ppb:
  - Flash yellow LED 3 times
  - Play sound 3
  - Report: 'Air quality degraded - recommend ventilation'

If BOTH are elevated:
  - Set red LED breathe
  - Play sound 8
  - Report: 'WARNING: Multiple air quality issues detected'"
```

### Barometric Pressure (Weather Prediction)

**Pressure Trend Analysis**
```
"Read barometric pressure every 10 minutes for 1 hour.
Track the pressure trend and predict weather:

Rapid fall (>3 hPa/hour):
  - Red LED
  - Sound 7
  - 'Storm system approaching - expect rain/wind'

Gradual fall (1-3 hPa/hour):
  - Yellow LED
  - Sound 4
  - 'Weather may deteriorate'

Rising (>1 hPa/hour):
  - Green LED breathe
  - Sound 1
  - 'Improving weather expected'

Stable (< 1 hPa change):
  - Blue LED
  - 'Weather stable'

Show current pressure and 1-hour change."
```

### Light Monitoring

**Daylight Tracker**
```
"Monitor light intensity throughout the day.

Morning (< 100 lux at 7 AM):
  - 'Overcast morning'
  - Orange LED

Mid-day (< 500 lux at noon):
  - 'Dark/cloudy day'
  - Yellow LED

Evening transition (drops below 50 lux):
  - 'Evening - lights recommended'
  - Warm white LED at 30%
  - Sound 2

Night (< 5 lux):
  - Turn off LED
  - 'Nighttime detected'

Report hourly summary."
```

**Color Temperature Detection**
```
"Read the RGB color sensor.
Analyze the ambient light color:

If red > blue + green:
  - 'Warm light detected (incandescent/sunset)'

If blue > red + green:
  - 'Cool light detected (daylight/LED)'

If red ≈ green ≈ blue:
  - 'Neutral/natural light'

Show R, G, B values and light temperature estimate."
```

## Motion & Orientation

### 3D Orientation Tracking

**Tilt Sensor**
```
"Read the Euler angles to detect device orientation:

If pitch > 45° or < -45°:
  - 'Device tilted forward/backward'
  - Red LED

If roll > 45° or < -45°:
  - 'Device tilted left/right'
  - Yellow LED

If pitch < 15° AND roll < 15°:
  - 'Device is level'
  - Green LED

Update every 2 seconds."
```

**Compass Navigation**
```
"Read the heading (compass direction).

Convert to cardinal directions:
- 0-22° or 338-360°: North
- 23-67°: Northeast
- 68-112°: East
- 113-157°: Southeast
- 158-202°: South
- 203-247°: Southwest
- 248-292°: West
- 293-337°: Northwest

Display: 'Device pointing [direction] ([degrees]°)'"
```

**Rotation Detection**
```
"Monitor quaternion for rotation changes.

When device rotates more than 45° from initial position:
  - Play sound 3
  - Flash LED based on rotation axis:
    * X-axis (pitch): Red
    * Y-axis (roll): Green
    * Z-axis (yaw): Blue

Reset baseline orientation on tap."
```

### Activity Detection

**Step Counter & Activity Level**
```
"Monitor step count and motion sensors:

Sedentary (0 steps in 30 min):
  - Blue LED breathe
  - Sound 2
  - 'No activity detected - time to move?'

Light activity (1-50 steps/30 min):
  - Green LED
  - 'Light activity level'

Moderate activity (51-200 steps/30 min):
  - Yellow LED
  - 'Moderate activity level'

High activity (>200 steps/30 min):
  - Orange LED breathe
  - 'High activity detected'

Update every 30 minutes."
```

**Tap/Knock Detection**
```
"Listen for tap events on the device.

Single tap:
  - Flash white LED once
  - Sound 1
  - Display current time and battery level

Double tap:
  - Read and display all environmental sensors
  - Green LED for 2 seconds

Triple tap:
  - Toggle between monitoring modes
  - Sound 4
  - Report current mode"
```

### Motion-Based Automation

**Anti-Theft Alarm**
```
"Create a motion-based security system:

1. Establish baseline (device should be stationary)
2. Monitor accelerometer for movement

If significant motion detected:
  - Red LED breathe (fast - 200ms)
  - Play sound 8 continuously
  - Report: 'ALERT: Movement detected!'
  - Show displacement magnitude

If orientation changes >30°:
  - 'Device has been moved/rotated!'

To disarm: Triple tap the device"
```

## Smart Alerts & Notifications

### Comfort Zone Monitor

```
"Create a comprehensive comfort monitoring system:

Check every 2 minutes:

Temperature: 20-24°C (ideal office temp)
Humidity: 40-60% (comfortable range)
CO2: < 1000 ppm (good air quality)
Light: 300-500 lux (good working light)

Status indicators:
- All ideal: Green LED breathe (slow)
- 1 parameter off: Yellow LED + sound 1
- 2 parameters off: Orange LED + sound 3
- 3+ parameters off: Red LED breathe + sound 8

Display detailed status with recommendations:
'Temperature: 26°C (HIGH - turn on AC)
Humidity: 45% (GOOD)
CO2: 1200 ppm (HIGH - open window)
Light: 450 lux (GOOD)'
"
```

### Multi-Condition Alerts

```
"Set up multi-factor environmental alerts:

CONDITION 1 - Stuffy room:
  IF temp >25°C AND CO2 >1200 ppm:
    - 'Room is hot and stuffy'
    - Red LED breathe
    - Sound 7
    - 'Open windows for ventilation!'

CONDITION 2 - Humid & warm (mold risk):
  IF temp >22°C AND humidity >70%:
    - 'High mold risk conditions'
    - Orange LED breathe
    - Sound 5
    - 'Increase ventilation/use dehumidifier'

CONDITION 3 - Cold & dry (discomfort):
  IF temp <18°C AND humidity <30%:
    - 'Cold and dry air'
    - Blue LED
    - Sound 2
    - 'Heating and humidifier recommended'

CONDITION 4 - Optimal conditions:
  IF all parameters in comfort range:
    - Green LED constant
    - Sound 1 (once)
    - 'Optimal environment achieved!'
"
```

### Progressive Warnings

```
"Create a graduated alert system for CO2:

First warning (1000 ppm):
  - Yellow LED for 5 seconds
  - Sound 1
  - 'CO2 elevated - consider ventilation'
  - Wait 10 minutes before next alert

Second warning (still >1000 after 10 min):
  - Yellow LED breathe
  - Sound 3
  - 'CO2 still elevated - open a window'
  - Wait 5 minutes

Third warning (still >1000 after 15 min):
  - Orange LED breathe
  - Sound 5
  - 'CO2 persistently high - urgent ventilation needed'
  - Alert every 5 minutes

Critical (>1500 ppm):
  - Red LED breathe (fast)
  - Sound 8
  - 'CRITICAL CO2 level - evacuate if necessary'
  - Alert every minute

Auto-reset when CO2 drops below 900 ppm:
  - Green LED flash 3 times
  - Sound 2
  - 'Air quality restored'"
```

## Multi-Sensor Workflows

### Smart Meeting Room Monitor

```
"Monitor meeting room conditions and occupancy:

OCCUPANCY DETECTION:
- Check step counter and motion sensors
- Monitor CO2 trend (rising = people present)
- Track light intensity (lights on/off)

OCCUPANCY STATUS:
Vacant:
  - CO2 < 600 ppm AND no motion for 15 min
  - Blue LED slow breathe
  - 'Room vacant'

Occupied (1-3 people):
  - CO2 600-900 ppm AND motion detected
  - Green LED
  - 'Room occupied - good conditions'

Occupied (4-8 people):
  - CO2 900-1200 ppm
  - Yellow LED if CO2 rising
  - 'Room getting crowded'

Overcrowded (>8 people):
  - CO2 >1200 ppm
  - Orange LED breathe
  - Sound 3
  - 'Room overcrowded - poor air quality'

COMFORT MONITORING:
- Temperature should be 20-22°C
- Humidity 40-60%
- Alert if conditions degraded

Every 5 minutes, display:
'Status: [Vacant/Occupied/Overcrowded]
Est. occupancy: [number] people (based on CO2)
Temperature: [temp]°C
CO2: [level] ppm
Air quality: [Excellent/Good/Moderate/Poor]'
"
```

### Plant Growth Monitor

```
"Create an automated plant care monitoring system:

ENVIRONMENTAL PARAMETERS:
Temperature: 18-28°C (optimal for most plants)
Humidity: 50-70% (tropical plants)
Light: >500 lux during day, <10 lux at night
CO2: Ambient levels (plants use CO2)

Check every hour:

EXCELLENT CONDITIONS (all optimal):
  - Green LED breathe (slow)
  - Sound 1 (once per day)
  - 'Perfect growing conditions!'

GOOD CONDITIONS (minor deviations):
  - Blue LED
  - 'Plants are happy'

NEEDS ATTENTION (1-2 parameters off):
  - Yellow LED
  - Sound 2
  - List issues: 'Low light - move to brighter location'
                 'High temperature - increase ventilation'
                 'Low humidity - mist plants'

POOR CONDITIONS (3+ parameters off):
  - Red LED breathe
  - Sound 5
  - 'PLANT STRESS: Multiple issues detected'
  - Detailed recommendations

NIGHT MODE (light < 10 lux):
  - Turn off LED (don't disturb plant darkness)
  - Continue monitoring
  - 'Night cycle - monitoring in dark mode'

DAYLIGHT HOURS (light > 100 lux):
  - Resume visual indicators
  - 'Daylight detected - plants photosynthesizing'

Track daily summary:
- Light hours
- Temperature range
- Humidity range
- Any stress periods
"
```

### Home Automation Trigger

```
"Use Thingy as a smart home automation controller:

MORNING ROUTINE (7-9 AM):
  When light >100 lux OR motion detected:
    - Green LED breathe
    - Sound 2
    - Trigger: 'Good morning! Starting day mode...'
    - Actions: Turn on lights, start coffee, etc.

AWAY MODE:
  No motion for 30 minutes:
    - Blue LED pulse
    - 'Entering away mode'
    - Check all sensors:
      * Temp >30°C: 'WARNING: High heat while away'
      * Humidity >80%: 'WARNING: Humidity spike'
      * Light change: 'Light activity detected'

EVENING MODE (light < 20 lux):
  - Warm white LED at 20%
  - Sound 1
  - 'Evening detected - entering night mode'

SLEEP MODE (no motion for 2 hours + dark):
  - Turn off LED
  - Continue sensor monitoring
  - Alert only for critical conditions

SECURITY MODE:
  - Monitor for unexpected motion
  - Track light changes (intruder detection)
  - Sound 8 + red LED if triggered
"
```

### Weather Station Complete

```
"Build a comprehensive weather monitoring station:

PRIMARY MEASUREMENTS:
1. Temperature (outdoor correlation)
2. Humidity
3. Barometric pressure (weather prediction)
4. Light intensity (cloud cover)

Every 10 minutes:

PRESSURE ANALYSIS:
  Calculate 3-hour pressure trend
  Rapid fall (>5 hPa/3hr): 'Storm approaching'
  Fall (2-5 hPa/3hr): 'Weather deteriorating'
  Stable (±1 hPa): 'Stable conditions'
  Rising (>2 hPa/3hr): 'Improving weather'

WEATHER PREDICTION:
  Falling pressure + humidity rising:
    - 'Rain likely within 12-24 hours'
    - Yellow LED

  Falling pressure + temperature drop:
    - 'Storm system approaching'
    - Red LED breathe
    - Sound 5

  Rising pressure + clear (high light):
    - 'Fair weather continuing'
    - Green LED

  High humidity + moderate temp + stable pressure:
    - 'Fog/mist possible'
    - Blue LED

DISPLAY FORMAT:
'Weather Station Report [HH:MM]
═══════════════════════════════
Temperature: 22.5°C
Humidity: 65%
Pressure: 1013.2 hPa (falling -2.3 hPa/3hr)
Light: 15,000 lux (bright sun)

Forecast: Weather deteriorating
Confidence: Moderate
Recommendation: Possible rain tonight

3-Hour Trend:
10:00  1015.5 hPa
11:00  1014.8 hPa
12:00  1014.1 hPa
13:00  1013.2 hPa (-2.3 hPa)
═══════════════════════════════'
"
```

## Advanced Automation

### Adaptive Office Comfort System

```
"Create an intelligent office environment controller:

LEARNING MODE (first week):
- Record preferred temperature range when manually adjusted
- Track productivity hours (high motion/activity)
- Note comfort complaints (manual interventions)

ADAPTIVE CONTROL:
Monitor every 5 minutes:

Time-based adjustments:
- Morning (7-9 AM): Target 21°C, higher CO2 tolerance
- Peak hours (9 AM-5 PM): Target 22°C, strict CO2 limits (<1000 ppm)
- Evening (5-7 PM): Target 23°C, relaxed monitoring

Multi-factor comfort score (0-100):
  Score = 0

  Temperature (20-24°C): +30 points
  Humidity (40-60%): +25 points
  CO2 (<800 ppm): +25 points
  Light (300-500 lux): +20 points

LED Indicator:
  90-100: Green breathe (slow) - 'Optimal'
  70-89: Blue - 'Good'
  50-69: Yellow - 'Fair'
  30-49: Orange breathe - 'Poor'
  0-29: Red breathe - 'Critical'

SMART ALERTS:
- Only alert if score drops 20+ points in 15 minutes
- Prioritize by urgency:
  1. CO2 >1500 ppm (immediate)
  2. Temp >28°C or <18°C (high)
  3. Humidity >70% or <30% (medium)
  4. Light issues (low)

DAILY REPORT (6 PM):
'Office Comfort Summary - [Date]
═══════════════════════════════
Peak Score: 95 (Excellent)
Low Score: 62 (Fair) at 2:30 PM
Average: 84

Issues today:
- 2:30 PM: CO2 spike (1350 ppm)
- 4:00 PM: High temp (26°C)

Recommendations:
- Improve mid-afternoon ventilation
- Consider AC adjustment

Tomorrow's forecast: Similar conditions expected'
"
```

### Laboratory Environmental Control

```
"Set up precision environmental monitoring for lab:

CRITICAL PARAMETERS:
Temperature: 20.0 ± 0.5°C (±2.5% tolerance)
Humidity: 45 ± 5% RH
Pressure: Track for altitude compensation
CO2: <600 ppm (cleanroom standard)

PRECISION MONITORING (every 1 minute):

TIER 1 ALERT (exceeds ±0.3°C or ±3% RH):
  - Yellow LED flash
  - Sound 2
  - 'WARNING: Approaching limit'
  - Log event with timestamp

TIER 2 ALERT (exceeds ±0.5°C or ±5% RH):
  - Orange LED breathe
  - Sound 5 (repeat every minute)
  - 'CRITICAL: Out of specification'
  - Recommend equipment shutdown

TIER 3 ALERT (exceeds ±1.0°C or ±8% RH):
  - Red LED breathe (fast)
  - Sound 8 (continuous)
  - 'EMERGENCY: Severe deviation'
  - 'Stop all experiments immediately'

STABILITY TRACKING:
- Calculate rolling 10-minute standard deviation
- If stddev > threshold: 'Unstable conditions'
- If stable for 30 min: Green LED + 'Conditions stable'

DATA LOGGING:
Every 5 minutes, record:
'[Timestamp],[Temp],[Humidity],[Pressure],[CO2],[Status]
2024-01-15 14:35:00,20.1,45.2,1013.2,450,STABLE
2024-01-15 14:40:00,20.3,45.8,1013.1,465,WARNING'

COMPLIANCE REPORT (hourly):
'Lab Environmental Report [HH:00]
═══════════════════════════════
Compliance Status: [PASS/FAIL]

Temperature: 20.2°C (20.0 ± 0.5°C) ✓
Range: 19.9 - 20.4°C
Std Dev: 0.12°C

Humidity: 44.8% RH (45 ± 5%) ✓
Range: 43.2 - 46.5%
Std Dev: 0.8%

Out-of-spec events: 2
Duration: 8 minutes total
Max deviation: +0.4°C at 13:42
"
```

### Energy Usage Correlator

```
"Use Thingy sensors to estimate HVAC energy usage:

BASELINE LEARNING:
- Record temperature when HVAC cycles on/off
- Track humidity changes during operation
- Monitor pressure (building pressurization)

HVAC STATUS INFERENCE:
Heating detected:
  IF temp rising >0.3°C/5min AND humidity dropping:
    - 'Heating system active'
    - Blue LED
    - Track runtime

Cooling detected:
  IF temp falling >0.3°C/5min AND humidity stable/dropping:
    - 'Cooling system active'
    - Cyan LED
    - Track runtime

Ventilation detected:
  IF CO2 dropping >50 ppm/10min:
    - 'Fresh air intake active'
    - Green LED pulse

ENERGY INSIGHTS:
Calculate daily HVAC runtime:
'Energy Usage Estimate - [Date]
═══════════════════════════════
Heating: 4.2 hours
Cooling: 2.1 hours
Ventilation: 6.5 hours

Efficiency notes:
- Peak cooling at 2 PM (highest outdoor temp)
- Morning heating 7-9 AM
- Continuous ventilation during occupancy

Recommendations:
- Pre-cool before 2 PM peak
- Reduce heating temp by 1°C to save 5-10% energy
- CO2 levels permit reduced ventilation rate

Estimated monthly cost: $XXX (based on runtime)
Savings potential: 15% with optimizations'
"
```

## Professional Applications

### Cleanroom Particle Monitor Proxy

```
"Use as a cleanroom environment validator:

ENVIRONMENTAL STANDARDS (ISO Class 7):
Temperature: 20 ± 2°C
Humidity: 45 ± 5% RH
Pressure: Positive (>1013 hPa indicates good sealing)
Air changes: Monitor via CO2 recovery rate

VALIDATION PROTOCOL:

ROOM INTEGRITY CHECK:
1. Measure baseline pressure
2. Seal room completely
3. Generate CO2 spike (breathing)
4. Monitor CO2 decay rate

CO2 decay analysis:
  Fast decay (>100 ppm/5min):
    - 'Good air exchange rate'
    - Green LED
  Moderate decay (50-100 ppm/5min):
    - 'Acceptable ventilation'
    - Yellow LED
  Slow decay (<50 ppm/5min):
    - 'Poor ventilation - check HVAC'
    - Red LED

ENVIRONMENTAL STABILITY:
Track all parameters every 30 seconds for 8 hours

Generate qualification report:
'Cleanroom Environmental Qualification
═══════════════════════════════
Date: [Date]
Duration: 8 hours (09:00-17:00)

Temperature Control:
  Target: 20 ± 2°C
  Actual range: 19.8 - 20.9°C
  Excursions: 0
  Status: PASS ✓

Humidity Control:
  Target: 45 ± 5% RH
  Actual range: 43.1 - 47.8%
  Excursions: 0
  Status: PASS ✓

Pressure Differential:
  Average: +12 Pa
  Minimum: +8 Pa
  Status: PASS ✓

Air Changes:
  Estimated: 20 ACH
  Standard: >15 ACH
  Status: PASS ✓

OVERALL: QUALIFIED ✓
Next validation: [Date + 6 months]'
"
```

### Wine Cellar Monitor

```
"Monitor wine storage conditions:

OPTIMAL WINE STORAGE:
Temperature: 12-14°C (ideal: 13°C)
Humidity: 60-70% (prevents cork drying)
Light: <5 lux (UV damages wine)
Vibration: Minimal (check via accelerometer)

MONITORING EVERY 30 MINUTES:

Temperature alerts:
  <10°C: 'Too cold - may slow aging'
  10-12°C: 'Cool - acceptable'
  12-14°C: 'Perfect storage temp' + Green LED
  14-16°C: 'Slightly warm' + Yellow LED
  >16°C: 'Too warm - wine aging accelerated' + Red LED

Humidity alerts:
  <50%: 'Low humidity - corks may dry' + Sound 3
  50-60%: 'Acceptable'
  60-70%: 'Optimal humidity' + Green LED
  70-80%: 'High humidity' + Yellow LED
  >80%: 'Risk of mold' + Red LED + Sound 5

Vibration detection:
  Check accelerometer variance
  High variance: 'Excessive vibration detected - check location'

Light exposure:
  Any light >10 lux: 'Light detected - ensure cellar door closed'

Temperature stability:
  Calculate daily range
  Range >2°C: 'Temperature unstable - check insulation'
  Range <1°C: 'Excellent stability'

MONTHLY REPORT:
'Wine Cellar Environmental Log - [Month]
═══════════════════════════════
Temperature:
  Average: 13.2°C ✓
  Range: 12.8 - 13.9°C ✓
  Stability: Excellent (±0.5°C)

Humidity:
  Average: 65% ✓
  Range: 62 - 68% ✓

Light exposure events: 3
  [Dates and durations]

Vibration events: 0 ✓

Conditions: OPTIMAL FOR AGING
Estimated aging rate: Normal
Collection value preserved: Yes ✓'
"
```

### Data Center Environmental Monitor

```
"Monitor server room conditions:

CRITICAL PARAMETERS:
Temperature: 18-27°C (ASHRAE guidelines)
Humidity: 40-60% RH (prevent static/condensation)
Dew point: <15°C (condensation risk)

REAL-TIME MONITORING (every 2 minutes):

TEMPERATURE ZONES:
  <18°C: 'Inefficient - overcooling'
  18-21°C: 'Optimal - energy efficient' + Green LED
  21-24°C: 'Acceptable' + Blue LED
  24-27°C: 'Warm - monitor closely' + Yellow LED
  27-30°C: 'Hot - increase cooling' + Orange LED + Sound 3
  >30°C: 'CRITICAL - equipment risk' + Red LED + Sound 8

DEW POINT CALCULATION:
  Calculate from temp + humidity
  Dew point approach (<5°C from temp):
    - 'WARNING: Condensation risk'
    - Flash yellow LED

THERMAL RUNAWAY DETECTION:
  If temp rising >2°C/10min:
    - 'ALERT: Rapid temperature rise'
    - 'Possible cooling failure or thermal event'
    - Red LED breathe
    - Sound 8 continuous

EFFICIENCY TRACKING:
  Monitor temperature stability
  Calculate PUE proxy (higher temp variance = lower efficiency)

ALERT ESCALATION:
  Level 1 (24°C): Email notification
  Level 2 (27°C): SMS + visual alert
  Level 3 (30°C): Call + sirens
  Level 4 (33°C): Emergency shutdown recommended

DAILY REPORT:
'Data Center Environmental Report
═══════════════════════════════
Uptime: 100%
Avg Temperature: 21.5°C ✓
Peak Temperature: 24.2°C (at 14:30)
Cooling efficiency: 94%

Humidity: 52% (stable) ✓
Dew point: 11°C (safe) ✓

Alerts: 1 (temp spike at 14:30)
Root cause: External temp +5°C

Recommendations:
- Increase cooling capacity 14:00-16:00
- Check hot aisle containment
- Consider additional CRAC unit'
"
```

## Creative Use Cases

### Musical Instrument

```
"Turn Thingy into a musical controller:

MOTION TO MUSIC:
- Pitch (forward/back tilt): Controls note pitch
- Roll (left/right tilt): Controls volume
- Yaw (rotation): Changes instrument/sound

When quaternion changes:
  Calculate angles from quaternion
  Map to musical parameters:

  Pitch angle (-90 to +90):
    Map to MIDI notes 60-84 (C4 to C6)

  Roll angle (-90 to +90):
    Map to volume 0-100

  Heading (0-360):
    Map to 8 sound samples

  Tap events:
    Play selected sound at calculated volume

GESTURE RECOGNITION:
  Quick forward tilt: Pitch up
  Quick backward tilt: Pitch down
  Shake: Random note
  Rotate 360°: Sound effect loop

Display:
'Musical Controller Active
═══════════════════════════════
Current note: E5 (MIDI 76)
Volume: 75%
Instrument: Sound 3
Last gesture: Shake
"
```

### Dice Simulator

```
"Electronic dice using motion sensors:

SHAKE TO ROLL:
Monitor accelerometer for shaking motion
High acceleration + rotation:
  - 'Rolling dice...'
  - LED cycles through rainbow colors
  - Play sound 6

After shake stops:
  Read heading angle (0-360°)
  Map to dice value:

  Heading 0-59°: Roll = 1
  Heading 60-119°: Roll = 2
  Heading 120-179°: Roll = 3
  Heading 180-239°: Roll = 4
  Heading 240-299°: Roll = 5
  Heading 300-359°: Roll = 6

Display result:
  1: Red LED
  2: Orange LED
  3: Yellow LED
  4: Green LED
  5: Blue LED
  6: Purple LED

Flash the color 3 times
Play corresponding sound (sound 1-6)

Show: 'You rolled a [number]!'

Track statistics:
'Dice Statistics
═══════════════════════════════
Total rolls: 47
1: 8 (17%)
2: 7 (15%)
3: 9 (19%)
4: 8 (17%)
5: 7 (15%)
6: 8 (17%)
Distribution: Fair ✓'
"
```

### Pomodoro Timer with Environment

```
"Create an enhanced Pomodoro technique timer:

CYCLE CONFIGURATION:
- Work: 25 minutes
- Short break: 5 minutes
- Long break: 15 minutes (every 4 cycles)

WORK SESSION:
  Start: Double-tap device
  - Green LED breathe (slow)
  - 'Focus session started'
  - Monitor environment:
    * Alert if CO2 >1200 ppm
    * Alert if temp uncomfortable
    * Track motion (ensure not sedentary)

  Every 10 min:
    - Brief green flash (progress indicator)

  5 min remaining:
    - Yellow LED breathe
    - 'Final push!'

  Session complete:
    - Sound 4
    - Flash green 3 times

SHORT BREAK (5 min):
  - Blue LED breathe
  - 'Break time - move around!'
  - Monitor step counter
  - If no steps after 3 min:
    * Sound 2
    * 'Remember to move!'

LONG BREAK (15 min):
  - Cyan LED breathe
  - Sound 5
  - 'Extended break - recharge!'
  - Suggest: drink water, fresh air

PRODUCTIVITY INSIGHTS:
'Pomodoro Session Summary
═══════════════════════════════
Sessions completed: 6/8
Total focus time: 150 minutes
Break compliance: 5/6 (83%)

Environment quality:
  Avg temp: 22°C ✓
  Avg CO2: 850 ppm ✓
  Interruptions: 2

Activity during breaks:
  Steps taken: 342 ✓
  Movement detected: Yes ✓

Productivity score: 92%
Recommendation: Excellent session!'
"
```

### Sleep Environment Optimizer

```
"Optimize bedroom environment for sleep:

IDEAL SLEEP CONDITIONS:
Temperature: 16-19°C (cooler for sleep)
Humidity: 30-50%
Light: <1 lux (complete darkness)
CO2: <1000 ppm
Sound: Quiet (use tap detection for noise)

BEDTIME ROUTINE (9 PM onwards):
  Monitor light levels

  When light <10 lux:
    - 'Preparing for sleep mode...'
    - Warm dim LED (5% red) for 10 minutes
    - Then turn off LED completely

  Enter monitoring mode:
    - Check conditions every 5 minutes
    - Only alert for critical issues

SLEEP QUALITY MONITORING:

Temperature optimization:
  16-18°C: 'Optimal sleep temperature' (silent)
  18-20°C: 'Acceptable'
  <16°C: Brief yellow flash (too cold)
  >20°C: Brief orange flash (too warm)

Disturbance detection:
  Light spike (>5 lux):
    - Log time and duration
    - 'Light disturbance at [time]'

  Motion/tap detected:
    - 'Movement at [time]'
    - Could indicate restlessness

  Temperature fluctuation (>2°C/hour):
    - 'Temperature instability'
    - May affect sleep quality

MORNING WAKE (7 AM):
  Gradual light simulation:
    - 6:45 AM: 1% warm white
    - 6:50 AM: 5% warm white
    - 6:55 AM: 10% warm white
    - 7:00 AM: 20% warm white
    - Gentle sound 1

SLEEP REPORT:
'Sleep Environment Report - [Night]
═══════════════════════════════
Sleep period: 10:15 PM - 6:45 AM (8h 30m)

Temperature:
  Start: 18.5°C
  Night low: 16.8°C (4 AM)
  End: 17.2°C
  Average: 17.5°C ✓

Humidity: 42% (stable) ✓

Disturbances:
  Light events: 2
    - 2:15 AM (3 seconds) - bathroom?
    - 5:30 AM (brief) - early dawn

  Movement: 4 times
    - Indicates good restful sleep

Air quality:
  CO2 max: 950 ppm ✓

Sleep quality score: 8.5/10 (Excellent)

Recommendations:
  - Environment ideal
  - Consider blackout curtains for dawn light
  - Continue current temperature setting'
"
```

## Best Practices

### Efficient Polling

```
"For continuous monitoring, use appropriate intervals:

Critical safety (CO2, temp in lab): Every 1-2 minutes
Environment comfort: Every 5 minutes
Weather trends: Every 10-15 minutes
Daily summaries: Once per hour
Battery conservation: Every 30 minutes

Too frequent polling drains battery and creates alert fatigue.
Balance responsiveness with practicality."
```

### Battery Management

```
"Monitor battery and adjust behavior:

At 100-80%: Normal operation
At 80-50%: Reduce polling frequency 50%
At 50-20%: Critical monitoring only, reduce LED brightness
At <20%: Minimal mode - essential alerts only

Show battery warning:
  'Battery at 25% - connect charger soon'
  Yellow LED flash once

Use LED efficiently:
  - Constant uses less power than breathe
  - Lower intensity saves battery
  - Turn off when not needed"
```

### Error Handling

```
"When a sensor read fails:

First failure:
  - Retry once after 2 seconds
  - If succeeds: Continue normally

Second failure:
  - Wait 10 seconds, retry
  - Yellow LED flash
  - 'Sensor read delayed'

Third failure:
  - Skip this sensor
  - Continue with others
  - 'Sensor temporarily unavailable - using last known value'

Connection lost:
  - Auto-reconnect (if enabled)
  - Show connection status
  - Queue sensor requests for after reconnect"
```

## Getting Creative

The Nordic Thingy:52 MCP Server gives you 25 tools to build unlimited automations. Combine sensors in novel ways:

- **Motion + Light + CO2** = Complete occupancy detection
- **Pressure + Humidity + Temp** = Weather forecasting
- **Quaternion + Tap** = Gesture recognition
- **All sensors + Time** = Predictive patterns
- **LED + Sound + Sensors** = Interactive feedback system

**What will you build?**

---

For more information, see the [README](README.md) and source code documentation.
