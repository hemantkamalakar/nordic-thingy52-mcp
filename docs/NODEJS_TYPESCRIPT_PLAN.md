# Nordic Thingy:52 MCP Server - Node.js TypeScript Implementation Plan

## Executive Summary

This document outlines a comprehensive plan for building a **Node.js TypeScript MCP (Model Context Protocol) server** for Nordic Thingy:52 IoT devices. This implementation will include **all features from the Python version (25+ tools)** plus **advanced capabilities unique to the Node.js ecosystem**, including real-time audio streaming, enhanced motion analytics, event-driven sensor subscriptions, and more.

**Target:** Feature-complete MCP server with 35+ tools, real-time event streaming, TypeScript type safety, and production-ready reliability.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Feature Comparison Matrix](#feature-comparison-matrix)
3. [Architecture Design](#architecture-design)
4. [Technology Stack](#technology-stack)
5. [Complete API Specification](#complete-api-specification)
6. [Data Models & Type Definitions](#data-models--type-definitions)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Code Examples](#code-examples)
9. [Testing Strategy](#testing-strategy)
10. [Deployment & Configuration](#deployment--configuration)

---

## 1. Project Overview

### Goals

1. **Feature Parity**: Implement all 25 tools from Python MCP server
2. **Advanced Features**: Add 10+ Node.js-exclusive features (microphone, advanced motion, real-time streaming)
3. **Type Safety**: Full TypeScript with strict type checking
4. **Event-Driven**: Real-time sensor subscriptions with WebSocket/SSE support
5. **Performance**: Sub-200ms response times, efficient event handling
6. **Production Ready**: Comprehensive error handling, logging, auto-reconnect, testing

### Key Advantages of Node.js Implementation

- **Event-Driven Architecture**: Native support for real-time sensor streaming
- **Microphone Audio**: Stream ADPCM audio data (16-bit, 16kHz) - **NOT in Python version**
- **Advanced Motion**: Rotation matrix, gravity vector, continuous streaming
- **Better LED Control**: Support for breathe, one-shot modes with proper parameters
- **Speaker PCM**: Direct PCM audio playback beyond preset sounds
- **Real-time Subscriptions**: Subscribe to sensor changes with event callbacks
- **TypeScript Types**: Complete type safety for all APIs and data structures
- **noble-device Library**: Mature, well-tested Nordic device integration

---

## 2. Feature Comparison Matrix

| Feature Category | Python Version | Node.js TypeScript Version | Status |
|-----------------|----------------|---------------------------|---------|
| **Device Management** | 6 tools | 8 tools | ✅ Enhanced |
| Device discovery | ✅ | ✅ + RSSI filtering | ✅ |
| Connection | ✅ | ✅ + auto-reconnect | ✅ |
| Disconnect | ✅ | ✅ | ✅ |
| Device status | ✅ | ✅ + firmware version | ✅ |
| Auto-reconnect config | ✅ | ✅ | ✅ |
| Cancel reconnect | ✅ | ✅ | ✅ |
| **Firmware info** | ❌ | ✅ | 🆕 |
| **Connection quality** | ❌ | ✅ (RSSI monitoring) | 🆕 |
| **Environmental Sensors** | 8 tools | 10 tools | ✅ Enhanced |
| Temperature | ✅ | ✅ + streaming | ✅ |
| Humidity | ✅ | ✅ + streaming | ✅ |
| Pressure | ✅ | ✅ + streaming | ✅ |
| Air quality (CO2/TVOC) | ✅ | ✅ + streaming | ✅ |
| Color sensor | ✅ | ✅ + LED calibration | ✅ |
| Light intensity | ✅ | ✅ | ✅ |
| All sensors | ✅ | ✅ | ✅ |
| **Subscribe to sensors** | ❌ | ✅ (real-time events) | 🆕 |
| **Configure intervals** | ❌ | ✅ (per-sensor polling) | 🆕 |
| **Gas sensor modes** | ❌ | ✅ | 🆕 |
| **Motion Sensors** | 6 tools | 12 tools | ✅ Enhanced |
| Raw motion (accel/gyro/mag) | ✅ | ✅ + streaming | ✅ |
| Quaternion | ✅ | ✅ + streaming | ✅ |
| Euler angles | ✅ | ✅ + streaming | ✅ |
| Heading | ✅ | ✅ + streaming | ✅ |
| Orientation | ✅ | ✅ + streaming | ✅ |
| Tap detection | ✅ | ✅ | ✅ |
| Step counter | ✅ | ✅ + interval config | ✅ |
| **Rotation matrix** | ❌ | ✅ | 🆕 |
| **Gravity vector** | ❌ | ✅ | 🆕 |
| **Motion processing config** | ❌ | ✅ (frequency, compensation) | 🆕 |
| **Wake on motion** | ❌ | ✅ | 🆕 |
| **Subscribe to motion** | ❌ | ✅ (real-time events) | 🆕 |
| **LED Control** | 3 tools | 5 tools | ✅ Enhanced |
| Set color (RGB) | ✅ | ✅ | ✅ |
| Breathe effect | ✅ (limited) | ✅ (full support) | ✅ |
| Turn off | ✅ | ✅ | ✅ |
| **One-shot flash** | ❌ | ✅ | 🆕 |
| **Color reference LED** | ❌ | ✅ (calibration) | 🆕 |
| **Sound** | 2 tools | 6 tools | ✅ Enhanced |
| Play preset sound | ✅ | ✅ | ✅ |
| Beep | ✅ | ✅ | ✅ |
| **Play custom tone** | ❌ | ✅ (frequency, duration) | 🆕 |
| **Stream PCM audio** | ❌ | ✅ | 🆕 |
| **Speaker mode config** | ❌ | ✅ | 🆕 |
| **Speaker status** | ❌ | ✅ (monitoring) | 🆕 |
| **Microphone** | 0 tools | 4 tools | 🆕 NEW |
| **Microphone enable/disable** | ❌ | ✅ | 🆕 |
| **Microphone streaming** | ❌ | ✅ (ADPCM, 16-bit) | 🆕 |
| **Microphone mode config** | ❌ | ✅ | 🆕 |
| **Save audio to file** | ❌ | ✅ | 🆕 |
| **Button** | 0 explicit tools | 2 tools | 🆕 Enhanced |
| **Button subscribe** | ❌ | ✅ (press/release events) | 🆕 |
| **Button polling** | ❌ | ✅ | 🆕 |
| **TOTAL TOOLS** | **25** | **47** | **+22 new** |

---

## 3. Architecture Design

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Layer                          │
│  (MCP Protocol, Tool Registration, Request Handling)         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 MCP Tools Layer                              │
│  - Device Management Tools (8 tools)                         │
│  - Environmental Sensor Tools (10 tools)                     │
│  - Motion Sensor Tools (12 tools)                            │
│  - LED Control Tools (5 tools)                               │
│  - Sound Tools (6 tools)                                     │
│  - Microphone Tools (4 tools)                                │
│  - Button Tools (2 tools)                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Business Logic Layer                            │
│  - ThingyClient class (wraps thingy52 library)              │
│  - Event managers for real-time subscriptions                │
│  - Data parsers and formatters                               │
│  - Connection manager with auto-reconnect                    │
│  - Error handling and retry logic                            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           Nordic thingy52 Library Layer                      │
│  (noble-device + noble for BLE communication)                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│            Bluetooth LE Hardware Layer                       │
│           (Nordic Thingy:52 Device)                          │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Directory Structure

```
thingy52-mcp-server/
├── src/
│   ├── index.ts                    # Main entry point
│   ├── server.ts                   # MCP server initialization
│   ├── tools/                      # MCP tool definitions
│   │   ├── device.tools.ts         # Device management tools
│   │   ├── environment.tools.ts    # Environmental sensor tools
│   │   ├── motion.tools.ts         # Motion sensor tools
│   │   ├── led.tools.ts            # LED control tools
│   │   ├── sound.tools.ts          # Sound tools
│   │   ├── microphone.tools.ts     # Microphone tools
│   │   └── button.tools.ts         # Button tools
│   ├── client/
│   │   ├── ThingyClient.ts         # Main client class
│   │   ├── ConnectionManager.ts    # Connection & reconnect logic
│   │   ├── EventManager.ts         # Event subscription management
│   │   └── SensorManager.ts        # Sensor enable/disable/config
│   ├── types/                      # TypeScript type definitions
│   │   ├── sensors.types.ts        # Sensor data types
│   │   ├── device.types.ts         # Device info types
│   │   ├── events.types.ts         # Event types
│   │   └── mcp.types.ts            # MCP tool types
│   ├── models/                     # Data validation models (Zod)
│   │   ├── environment.models.ts
│   │   ├── motion.models.ts
│   │   └── device.models.ts
│   ├── constants/
│   │   ├── uuids.ts                # Bluetooth UUIDs
│   │   ├── colors.ts               # LED color presets
│   │   └── config.ts               # Configuration constants
│   ├── utils/
│   │   ├── logger.ts               # Winston logging
│   │   ├── parsers.ts              # Data parsing utilities
│   │   └── validators.ts           # Input validation
│   └── config/
│       └── server.config.ts        # Server configuration
├── tests/
│   ├── unit/
│   │   ├── client.test.ts
│   │   ├── parsers.test.ts
│   │   └── validators.test.ts
│   ├── integration/
│   │   ├── sensors.test.ts
│   │   ├── actuators.test.ts
│   │   └── events.test.ts
│   └── e2e/
│       └── mcp.test.ts
├── examples/
│   ├── basic-usage.ts
│   ├── real-time-streaming.ts
│   ├── audio-recording.ts
│   └── automation-rules.ts
├── docs/
│   ├── API.md
│   ├── EXAMPLES.md
│   └── DEPLOYMENT.md
├── package.json
├── tsconfig.json
├── .eslintrc.js
├── .prettierrc
└── README.md
```

### 3.3 Component Responsibilities

#### MCP Server Layer (`src/server.ts`)
- Initialize MCP server using `@modelcontextprotocol/sdk`
- Register all 47 tools with proper typing
- Handle MCP protocol messages (requests, notifications)
- Manage server lifecycle (startup, shutdown)

#### Tools Layer (`src/tools/*.tools.ts`)
- Define MCP tool schemas with Zod validation
- Implement tool handler functions
- Format responses for Claude consumption
- Handle errors gracefully with user-friendly messages

#### Business Logic Layer (`src/client/`)
- **ThingyClient**: Main interface to thingy52 library
- **ConnectionManager**: Handle discovery, connect, disconnect, auto-reconnect
- **EventManager**: Manage event subscriptions and callbacks
- **SensorManager**: Enable/disable sensors, configure intervals

#### Types Layer (`src/types/`)
- Complete TypeScript type definitions for all data structures
- Sensor data interfaces
- Event callback signatures
- MCP tool input/output types

---

## 4. Technology Stack

### Core Dependencies

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.20.1",
    "thingy52": "^1.0.4",
    "noble-device": "^1.4.1",
    "@abandonware/noble": "^1.9.2-26",
    "zod": "^4.1.12",
    "winston": "^3.18.3",
    "dotenv": "^16.4.5"
  },
  "devDependencies": {
    "typescript": "^5.9.3",
    "@types/node": "^22.10.0",
    "@types/noble-device": "^1.0.0",
    "tsx": "^4.19.2",
    "vitest": "^3.2.4",
    "@vitest/coverage-v8": "^3.2.4",
    "eslint": "^9.18.0",
    "@typescript-eslint/eslint-plugin": "^8.20.0",
    "@typescript-eslint/parser": "^8.20.0",
    "prettier": "^3.4.2"
  }
}
```

### Key Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| `@modelcontextprotocol/sdk` | MCP server implementation | 1.20.1 |
| `thingy52` | Nordic Thingy:52 BLE library | 1.0.4 |
| `noble-device` | BLE device abstraction | 1.4.1 |
| `@abandonware/noble` | Modern BLE central module (actively maintained) | 1.9.2-26 |
| `zod` | Runtime type validation (v4 with performance improvements) | 4.1.12 |
| `winston` | Structured logging | 3.18.3 |
| `typescript` | Type safety (v5.9 with node20 module support) | 5.9.3 |
| `vitest` | Testing framework (v3 with improved browser mode) | 3.2.4 |

---

## 5. Complete API Specification

### 5.1 Device Management Tools (8 tools)

#### `scan_devices`
```typescript
interface ScanDevicesInput {
  timeout?: number;          // Scan duration in seconds (default: 10)
  rssiThreshold?: number;    // Minimum RSSI to include (default: -100)
}

interface ScanDevicesOutput {
  devices: DeviceInfo[];
  count: number;
  duration: number;
}

interface DeviceInfo {
  address: string;
  name: string;
  rssi: number;
  connectable: boolean;
}
```

#### `connect_device`
```typescript
interface ConnectDeviceInput {
  address: string;
  timeout?: number;          // Connection timeout (default: 30s)
}

interface ConnectDeviceOutput {
  success: boolean;
  address: string;
  name?: string;
  firmwareVersion?: string;
  message: string;
}
```

#### `disconnect_device`
```typescript
interface DisconnectDeviceOutput {
  success: boolean;
  message: string;
}
```

#### `get_device_status`
```typescript
interface DeviceStatusOutput {
  connected: boolean;
  connectionState: 'connected' | 'disconnected' | 'reconnecting' | 'manual_disconnect';
  address?: string;
  name?: string;
  batteryLevel?: number;     // 0-100%
  firmwareVersion?: string;
  rssi?: number;
  reconnecting?: boolean;
  retryCount?: number;
}
```

#### `get_firmware_info` 🆕
```typescript
interface FirmwareInfoOutput {
  version: string;
  manufacturer: string;
  model: string;
  serialNumber?: string;
}
```

#### `configure_auto_reconnect`
```typescript
interface AutoReconnectConfig {
  enabled: boolean;
  maxAttempts?: number;      // 0 = infinite
  initialDelay?: number;     // seconds
  maxDelay?: number;         // seconds
}
```

#### `cancel_reconnect_attempts`
```typescript
interface CancelReconnectOutput {
  success: boolean;
  message: string;
}
```

#### `monitor_connection_quality` 🆕
```typescript
interface ConnectionQualityInput {
  interval?: number;         // Monitoring interval in seconds
}

interface ConnectionQualityOutput {
  rssi: number;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
  packetLoss?: number;       // percentage
  latency?: number;          // milliseconds
}
```

### 5.2 Environmental Sensor Tools (10 tools)

#### `read_temperature`
```typescript
interface TemperatureOutput {
  temperature_celsius: number;
  unit: string;
  timestamp: Date;
}
```

#### `read_humidity`
```typescript
interface HumidityOutput {
  humidity_percent: number;
  unit: string;
  timestamp: Date;
}
```

#### `read_pressure`
```typescript
interface PressureOutput {
  pressure_hpa: number;
  unit: string;
  timestamp: Date;
}
```

#### `read_air_quality`
```typescript
interface AirQualityOutput {
  co2_ppm: number;
  tvoc_ppb: number;
  air_quality_status: 'excellent' | 'good' | 'acceptable' | 'poor' | 'bad';
  timestamp: Date;
}
```

#### `read_color_sensor`
```typescript
interface ColorSensorOutput {
  red: number;               // 0-65535
  green: number;
  blue: number;
  clear: number;             // Light intensity
  timestamp: Date;
}
```

#### `read_light_intensity`
```typescript
interface LightIntensityOutput {
  light_intensity_lux: number;
  unit: string;
  timestamp: Date;
}
```

#### `read_all_sensors`
```typescript
interface AllSensorsOutput {
  temperature: number;
  humidity: number;
  pressure: number;
  co2: number;
  tvoc: number;
  timestamp: Date;
}
```

#### `subscribe_to_sensors` 🆕
```typescript
interface SubscribeInput {
  sensors: ('temperature' | 'humidity' | 'pressure' | 'gas' | 'color')[];
  callback: (data: SensorData) => void;
}

interface SubscribeOutput {
  subscriptionId: string;
  sensors: string[];
  message: string;
}
```

#### `configure_sensor_intervals` 🆕
```typescript
interface SensorIntervalsInput {
  temperature?: number;      // milliseconds
  humidity?: number;
  pressure?: number;
  gas?: number;
  color?: number;
}

interface SensorIntervalsOutput {
  success: boolean;
  intervals: Record<string, number>;
}
```

#### `set_gas_sensor_mode` 🆕
```typescript
interface GasSensorModeInput {
  mode: 1 | 2 | 3;          // Different sensitivity modes
}

interface GasSensorModeOutput {
  success: boolean;
  mode: number;
  message: string;
}
```

### 5.3 Motion Sensor Tools (12 tools)

#### `read_raw_motion`
```typescript
interface RawMotionOutput {
  accelerometer: { x: number; y: number; z: number };
  gyroscope: { x: number; y: number; z: number };
  magnetometer: { x: number; y: number; z: number };
  timestamp: Date;
}
```

#### `read_quaternion`
```typescript
interface QuaternionOutput {
  w: number;
  x: number;
  y: number;
  z: number;
  format: string;
  timestamp: Date;
}
```

#### `read_euler_angles`
```typescript
interface EulerAnglesOutput {
  roll_degrees: number;
  pitch_degrees: number;
  yaw_degrees: number;
  unit: string;
  timestamp: Date;
}
```

#### `read_heading`
```typescript
interface HeadingOutput {
  heading_degrees: number;   // 0-360
  unit: string;
  range: string;
  timestamp: Date;
}
```

#### `read_orientation`
```typescript
interface OrientationOutput {
  orientation: 'portrait' | 'landscape' | 'reverse_portrait' | 'reverse_landscape';
  orientationCode: number;
  timestamp: Date;
}
```

#### `read_tap_event`
```typescript
interface TapEventInput {
  timeout?: number;          // seconds to wait
}

interface TapEventOutput {
  tapDetected: boolean;
  type?: 'single' | 'double';
  direction?: string;
  count?: number;
  timestamp?: Date;
}
```

#### `read_step_count`
```typescript
interface StepCountOutput {
  steps: number;
  elapsedTime?: number;      // milliseconds
  timestamp: Date;
}
```

#### `read_rotation_matrix` 🆕
```typescript
interface RotationMatrixOutput {
  matrix: number[][];        // 3x3 rotation matrix
  timestamp: Date;
}
```

#### `read_gravity_vector` 🆕
```typescript
interface GravityVectorOutput {
  x: number;
  y: number;
  z: number;
  magnitude: number;
  timestamp: Date;
}
```

#### `configure_motion_processing` 🆕
```typescript
interface MotionProcessingInput {
  frequency?: number;        // Hz (200, 100, 50, 25, 5)
  tempCompensationInterval?: number;  // ms
  magnetometerCompensationInterval?: number;  // ms
}

interface MotionProcessingOutput {
  success: boolean;
  config: MotionProcessingInput;
}
```

#### `set_wake_on_motion` 🆕
```typescript
interface WakeOnMotionInput {
  enabled: boolean;
}

interface WakeOnMotionOutput {
  success: boolean;
  enabled: boolean;
}
```

#### `subscribe_to_motion` 🆕
```typescript
interface MotionSubscribeInput {
  motionTypes: ('raw' | 'quaternion' | 'euler' | 'heading' | 'orientation' | 'gravity' | 'rotation')[];
  callback: (data: MotionData) => void;
}

interface MotionSubscribeOutput {
  subscriptionId: string;
  motionTypes: string[];
}
```

### 5.4 LED Control Tools (5 tools)

#### `set_led_color`
```typescript
interface SetLedColorInput {
  color?: string;            // Named color
  red?: number;              // 0-255
  green?: number;
  blue?: number;
  intensity?: number;        // 0-100
}

interface SetLedColorOutput {
  success: boolean;
  message: string;
  rgb?: [number, number, number];
}
```

#### `set_led_breathe`
```typescript
interface SetLedBreatheInput {
  color: string;
  intensity?: number;        // 0-100
  delay?: number;            // milliseconds
}

interface SetLedBreatheOutput {
  success: boolean;
  message: string;
}
```

#### `turn_off_led`
```typescript
interface TurnOffLedOutput {
  success: boolean;
  message: string;
}
```

#### `set_led_one_shot` 🆕
```typescript
interface SetLedOneShotInput {
  color: string;
  intensity?: number;        // 0-100
}

interface SetLedOneShotOutput {
  success: boolean;
  message: string;
}
```

#### `set_color_reference_led` 🆕
```typescript
interface ColorReferenceLedInput {
  red: number;               // 0-255
  green: number;
  blue: number;
}

interface ColorReferenceLedOutput {
  success: boolean;
  message: string;
}
```

### 5.5 Sound Tools (6 tools)

#### `play_sound`
```typescript
interface PlaySoundInput {
  soundId: number;           // 1-8
}

interface PlaySoundOutput {
  success: boolean;
  message: string;
}
```

#### `beep`
```typescript
interface BeepOutput {
  success: boolean;
  message: string;
}
```

#### `play_tone` 🆕
```typescript
interface PlayToneInput {
  frequency: number;         // Hz
  duration: number;          // milliseconds
  volume?: number;           // 0-100
}

interface PlayToneOutput {
  success: boolean;
  message: string;
}
```

#### `stream_pcm_audio` 🆕
```typescript
interface StreamPcmAudioInput {
  pcmData: Buffer;           // PCM audio buffer
  sampleRate?: number;       // Default: 16000 Hz
}

interface StreamPcmAudioOutput {
  success: boolean;
  bytesWritten: number;
  message: string;
}
```

#### `set_speaker_mode` 🆕
```typescript
interface SpeakerModeInput {
  mode: number;              // Speaker operation mode
}

interface SpeakerModeOutput {
  success: boolean;
  mode: number;
}
```

#### `get_speaker_status` 🆕
```typescript
interface SpeakerStatusOutput {
  status: number;
  playing: boolean;
  message: string;
}
```

### 5.6 Microphone Tools (4 tools) 🆕 NEW CATEGORY

#### `enable_microphone` 🆕
```typescript
interface EnableMicrophoneOutput {
  success: boolean;
  format: string;            // "ADPCM 16-bit 16kHz"
  message: string;
}
```

#### `disable_microphone` 🆕
```typescript
interface DisableMicrophoneOutput {
  success: boolean;
  message: string;
}
```

#### `stream_microphone` 🆕
```typescript
interface StreamMicrophoneInput {
  callback: (audioData: Buffer) => void;
  format?: 'adpcm' | 'pcm';
}

interface StreamMicrophoneOutput {
  streamId: string;
  format: string;
  sampleRate: number;
  message: string;
}
```

#### `record_audio_to_file` 🆕
```typescript
interface RecordAudioInput {
  duration: number;          // seconds
  outputPath: string;
  format?: 'wav' | 'raw';
}

interface RecordAudioOutput {
  success: boolean;
  filePath: string;
  duration: number;
  fileSize: number;
}
```

### 5.7 Button Tools (2 tools) 🆕

#### `subscribe_to_button` 🆕
```typescript
interface SubscribeToButtonInput {
  callback: (event: ButtonEvent) => void;
}

interface SubscribeToButtonOutput {
  subscriptionId: string;
  message: string;
}

interface ButtonEvent {
  state: 'pressed' | 'released';
  timestamp: Date;
}
```

#### `get_button_state` 🆕
```typescript
interface ButtonStateOutput {
  state: 'pressed' | 'released';
  lastChanged?: Date;
}
```

---

## 6. Data Models & Type Definitions

### 6.1 Core Type Definitions (`src/types/`)

```typescript
// src/types/sensors.types.ts

export interface EnvironmentalData {
  temperature?: number;
  humidity?: number;
  pressure?: number;
  co2?: number;
  tvoc?: number;
  timestamp: Date;
}

export interface MotionData {
  accelerometer?: Vector3D;
  gyroscope?: Vector3D;
  magnetometer?: Vector3D;
  quaternion?: Quaternion;
  euler?: EulerAngles;
  heading?: number;
  orientation?: Orientation;
  gravity?: Vector3D;
  rotation?: Matrix3x3;
  timestamp: Date;
}

export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface Quaternion {
  w: number;
  x: number;
  y: number;
  z: number;
}

export interface EulerAngles {
  roll: number;
  pitch: number;
  yaw: number;
}

export type Orientation = 'portrait' | 'landscape' | 'reverse_portrait' | 'reverse_landscape';

export type Matrix3x3 = [[number, number, number], [number, number, number], [number, number, number]];

export interface ColorData {
  red: number;
  green: number;
  blue: number;
  clear: number;
}

export interface AudioData {
  format: 'ADPCM' | 'PCM';
  sampleRate: number;
  buffer: Buffer;
  timestamp: Date;
}
```

```typescript
// src/types/device.types.ts

export interface DeviceInfo {
  address: string;
  name: string;
  rssi: number;
  connectable: boolean;
  firmwareVersion?: string;
  manufacturer?: string;
}

export interface ConnectionStatus {
  connected: boolean;
  state: ConnectionState;
  address?: string;
  name?: string;
  batteryLevel?: number;
  rssi?: number;
  firmwareVersion?: string;
  reconnecting?: boolean;
  retryCount?: number;
  lastConnected?: Date;
}

export type ConnectionState = 'connected' | 'disconnected' | 'reconnecting' | 'manual_disconnect';

export interface AutoReconnectConfig {
  enabled: boolean;
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
}
```

```typescript
// src/types/events.types.ts

export type SensorEventType =
  | 'temperature'
  | 'humidity'
  | 'pressure'
  | 'gas'
  | 'color'
  | 'button'
  | 'motion'
  | 'tap'
  | 'stepCounter'
  | 'microphone';

export interface SensorEvent<T = any> {
  type: SensorEventType;
  data: T;
  timestamp: Date;
}

export type EventCallback<T = any> = (event: SensorEvent<T>) => void;

export interface Subscription {
  id: string;
  type: SensorEventType;
  callback: EventCallback;
  active: boolean;
}
```

### 6.2 Zod Validation Schemas (`src/models/`)

```typescript
// src/models/environment.models.ts

import { z } from 'zod';

// Zod v4 with improved performance and new features
export const TemperatureSchema = z.object({
  temperature_celsius: z.number().min(-40).max(85),
  unit: z.literal('°C'),
  timestamp: z.date()
});

export const HumiditySchema = z.object({
  humidity_percent: z.number().min(0).max(100),
  unit: z.literal('%'),
  timestamp: z.date()
});

export const PressureSchema = z.object({
  pressure_hpa: z.number().min(260).max(1260),
  unit: z.literal('hPa'),
  timestamp: z.date()
});

export const AirQualitySchema = z.object({
  co2_ppm: z.number().min(400).max(8192),
  tvoc_ppb: z.number().min(0).max(1187),
  air_quality_status: z.enum(['excellent', 'good', 'acceptable', 'poor', 'bad']),
  timestamp: z.date()
});

export const ColorSensorSchema = z.object({
  red: z.number().int().min(0).max(65535),
  green: z.number().int().min(0).max(65535),
  blue: z.number().int().min(0).max(65535),
  clear: z.number().int().min(0).max(65535),
  timestamp: z.date()
});
```

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal**: Basic MCP server with device management and simple sensors

- [ ] Project setup (TypeScript, dependencies, configuration)
- [ ] MCP server initialization with `@modelcontextprotocol/sdk`
- [ ] ThingyClient class wrapping thingy52 library
- [ ] Device management tools (scan, connect, disconnect, status)
- [ ] Basic environmental sensors (temperature, humidity, pressure)
- [ ] Type definitions and Zod schemas
- [ ] Logger setup (Winston)
- [ ] Basic error handling
- [ ] Unit tests for core functionality

**Deliverables**:
- Working MCP server with 10+ tools
- TypeScript compilation successful
- Basic tests passing

### Phase 2: Advanced Sensors & LED (Week 3-4)

**Goal**: Complete sensor suite and LED control

- [ ] Air quality sensor (CO2, TVOC)
- [ ] Color sensor with calibration
- [ ] All motion sensors (raw, quaternion, euler, heading, orientation, tap, steps)
- [ ] LED control (color, breathe, one-shot, turn off, reference)
- [ ] Sound playback (preset sounds, beep)
- [ ] Sensor interval configuration
- [ ] Gas sensor mode configuration
- [ ] Integration tests with hardware

**Deliverables**:
- 30+ tools implemented
- All Python-equivalent features complete

### Phase 3: Event System & Real-Time Streaming (Week 5-6)

**Goal**: Event-driven architecture with subscriptions

- [ ] EventManager class for pub-sub pattern
- [ ] Sensor subscription tools
- [ ] Motion subscription tools
- [ ] Button event subscription
- [ ] Real-time data streaming
- [ ] WebSocket/SSE support (optional)
- [ ] Event buffering and management
- [ ] Performance optimization

**Deliverables**:
- Event-driven architecture working
- Real-time sensor streaming
- Subscription management

### Phase 4: Audio & Advanced Motion (Week 7-8)

**Goal**: Microphone streaming and advanced motion features

- [ ] Microphone enable/disable
- [ ] Microphone audio streaming (ADPCM)
- [ ] Audio recording to file
- [ ] PCM audio playback
- [ ] Custom tone generation
- [ ] Speaker mode and status
- [ ] Rotation matrix calculation
- [ ] Gravity vector
- [ ] Motion processing configuration
- [ ] Wake on motion

**Deliverables**:
- Audio features working
- Advanced motion sensors operational
- 45+ tools total

### Phase 5: Connection Management & Reliability (Week 9-10)

**Goal**: Production-ready reliability features

- [ ] Auto-reconnect with exponential backoff
- [ ] Connection quality monitoring
- [ ] RSSI tracking
- [ ] Firmware version detection
- [ ] Comprehensive error handling
- [ ] Retry logic for failed operations
- [ ] Connection state management
- [ ] Graceful degradation

**Deliverables**:
- Auto-reconnect working
- Connection stability features
- Error recovery mechanisms

### Phase 6: Testing & Documentation (Week 11-12)

**Goal**: Production quality with comprehensive testing

- [ ] Unit tests (90%+ coverage)
- [ ] Integration tests with hardware
- [ ] E2E tests via MCP protocol
- [ ] Performance benchmarks
- [ ] API documentation
- [ ] Usage examples
- [ ] Deployment guide
- [ ] CI/CD setup

**Deliverables**:
- 90%+ test coverage
- Complete documentation
- Ready for production deployment

---

## 8. Code Examples

### 8.1 Basic Usage Example

```typescript
// examples/basic-usage.ts

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { ThingyClient } from './src/client/ThingyClient.js';

// Using @modelcontextprotocol/sdk v1.20.1
async function main() {
  const server = new Server(
    {
      name: 'Nordic Thingy:52',
      version: '1.0.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  const thingyClient = new ThingyClient({
    autoReconnect: true,
    maxReconnectAttempts: 10
  });

  // Register tools
  // ... (tool registration code)

  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.log('MCP Server started and listening for requests...');
}

main().catch(console.error);
```

### 8.2 ThingyClient Implementation

```typescript
// src/client/ThingyClient.ts

import Thingy from 'thingy52';
import { EventEmitter } from 'events';
import { DeviceInfo, ConnectionStatus, EnvironmentalData } from '../types';

export class ThingyClient extends EventEmitter {
  private device: any = null;
  private connected: boolean = false;
  private lastAddress: string | null = null;
  private subscriptions: Map<string, any> = new Map();

  async scan(timeout: number = 10, rssiThreshold: number = -100): Promise<DeviceInfo[]> {
    return new Promise((resolve, reject) => {
      const devices: DeviceInfo[] = [];
      const timeoutId = setTimeout(() => {
        resolve(devices);
      }, timeout * 1000);

      Thingy.discover((device) => {
        if (device.rssi >= rssiThreshold) {
          devices.push({
            address: device.address,
            name: device.name || 'Thingy:52',
            rssi: device.rssi,
            connectable: true
          });
        }
      });
    });
  }

  async connect(address: string, timeout: number = 30): Promise<boolean> {
    return new Promise((resolve, reject) => {
      Thingy.discoverById(address, (device) => {
        device.connectAndSetUp((error) => {
          if (error) {
            reject(error);
            return;
          }

          this.device = device;
          this.connected = true;
          this.lastAddress = address;

          // Setup disconnect handler
          device.on('disconnect', () => this.handleDisconnect());

          resolve(true);
        });
      });

      setTimeout(() => reject(new Error('Connection timeout')), timeout * 1000);
    });
  }

  async disconnect(): Promise<boolean> {
    if (this.device && this.connected) {
      return new Promise((resolve) => {
        this.device.disconnect(() => {
          this.connected = false;
          this.device = null;
          resolve(true);
        });
      });
    }
    return false;
  }

  private handleDisconnect(): void {
    this.connected = false;
    this.emit('disconnected', { address: this.lastAddress });
    // Trigger auto-reconnect if enabled
    if (this.autoReconnectEnabled) {
      this.startAutoReconnect();
    }
  }

  async readTemperature(): Promise<number> {
    return new Promise((resolve, reject) => {
      if (!this.connected) {
        reject(new Error('Not connected to device'));
        return;
      }

      this.device.temperature_enable((error) => {
        if (error) {
          reject(error);
          return;
        }

        this.device.once('temperatureNotif', (temp: number) => {
          this.device.temperature_disable(() => {});
          resolve(temp);
        });
      });
    });
  }

  async subscribeToTemperature(callback: (temp: number) => void): Promise<string> {
    const subscriptionId = this.generateSubscriptionId();

    await new Promise((resolve, reject) => {
      this.device.temperature_enable((error) => {
        if (error) reject(error);
        else resolve(true);
      });
    });

    const handler = (temp: number) => callback(temp);
    this.device.on('temperatureNotif', handler);

    this.subscriptions.set(subscriptionId, {
      type: 'temperature',
      handler,
      unsubscribe: () => {
        this.device.removeListener('temperatureNotif', handler);
        this.device.temperature_disable(() => {});
      }
    });

    return subscriptionId;
  }

  async unsubscribe(subscriptionId: string): Promise<boolean> {
    const subscription = this.subscriptions.get(subscriptionId);
    if (subscription) {
      subscription.unsubscribe();
      this.subscriptions.delete(subscriptionId);
      return true;
    }
    return false;
  }

  private generateSubscriptionId(): string {
    return `sub_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // ... Additional methods for other sensors and actuators
}
```

### 8.3 MCP Tool Definition Example

```typescript
// src/tools/environment.tools.ts

import { z } from 'zod';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { ThingyClient } from '../client/ThingyClient.js';
import { TemperatureSchema } from '../models/environment.models.js';

// Using MCP SDK v1.20.1 with proper tool registration
export function registerEnvironmentTools(server: any, client: ThingyClient) {

  // Register read_temperature tool
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: 'read_temperature',
        description: 'Read the current temperature from the Thingy:52 device',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'subscribe_to_sensors',
        description: 'Subscribe to real-time environmental sensor updates',
        inputSchema: {
          type: 'object',
          properties: {
            sensors: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['temperature', 'humidity', 'pressure', 'gas', 'color']
              }
            },
            interval: {
              type: 'number',
              default: 1000
            }
          },
          required: ['sensors']
        }
      }
    ]
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name === 'read_temperature') {
      try {
        const temp = await client.readTemperature();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              temperature_celsius: temp,
              unit: '°C',
              timestamp: new Date()
            })
          }]
        };
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: `Error: Failed to read temperature: ${error instanceof Error ? error.message : String(error)}`
          }],
          isError: true
        };
      }
    }

    if (request.params.name === 'subscribe_to_sensors') {
      const { sensors, interval = 1000 } = request.params.arguments as {
        sensors: string[];
        interval?: number;
      };

      const subscriptionIds: string[] = [];

      for (const sensor of sensors) {
        let subId: string;
        switch (sensor) {
          case 'temperature':
            await client.setTemperatureInterval(interval);
            subId = await client.subscribeToTemperature((temp) => {
              // Emit event or send via WebSocket
              client.emit('sensor_data', { type: 'temperature', value: temp });
            });
            subscriptionIds.push(subId);
            break;
          // ... other sensors
        }
      }

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            subscriptionId: subscriptionIds.join(','),
            sensors,
            message: `Subscribed to ${sensors.length} sensor(s)`
          })
        }]
      };
    }

    throw new Error(`Unknown tool: ${request.params.name}`);
  });
}
```

### 8.4 Real-Time Streaming Example

```typescript
// examples/real-time-streaming.ts

import { ThingyClient } from '../src/client/ThingyClient';

async function streamSensors() {
  const client = new ThingyClient();

  // Scan and connect
  const devices = await client.scan(10);
  if (devices.length === 0) {
    console.error('No Thingy devices found');
    return;
  }

  await client.connect(devices[0].address);
  console.log(`Connected to ${devices[0].name}`);

  // Subscribe to multiple sensors
  const tempSubId = await client.subscribeToTemperature((temp) => {
    console.log(`Temperature: ${temp}°C`);
  });

  const humiditySubId = await client.subscribeToHumidity((humidity) => {
    console.log(`Humidity: ${humidity}%`);
  });

  const motionSubId = await client.subscribeToRawMotion((motion) => {
    console.log(`Accel: X=${motion.accelerometer.x}, Y=${motion.accelerometer.y}, Z=${motion.accelerometer.z}`);
  });

  // Configure update intervals
  await client.setTemperatureInterval(2000);  // 2 seconds
  await client.setHumidityInterval(2000);

  // Stream for 60 seconds
  await new Promise(resolve => setTimeout(resolve, 60000));

  // Cleanup
  await client.unsubscribe(tempSubId);
  await client.unsubscribe(humiditySubId);
  await client.unsubscribe(motionSubId);
  await client.disconnect();
}

streamSensors().catch(console.error);
```

### 8.5 Audio Recording Example

```typescript
// examples/audio-recording.ts

import { ThingyClient } from '../src/client/ThingyClient';
import * as fs from 'fs';

async function recordAudio() {
  const client = new ThingyClient();

  // Connect to device
  const devices = await client.scan(10);
  await client.connect(devices[0].address);

  // Record 10 seconds of audio
  const audioFile = await client.recordAudioToFile({
    duration: 10,
    outputPath: './recording.wav',
    format: 'wav'
  });

  console.log(`Audio recorded: ${audioFile.filePath} (${audioFile.fileSize} bytes)`);

  await client.disconnect();
}

recordAudio().catch(console.error);
```

---

## 9. Testing Strategy

### 9.1 Test Coverage Goals

- **Unit Tests**: 90%+ coverage
- **Integration Tests**: All hardware features
- **E2E Tests**: MCP protocol compliance
- **Performance Tests**: Response times, throughput

### 9.2 Test Structure

```typescript
// tests/unit/client.test.ts

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { ThingyClient } from '../../src/client/ThingyClient';

describe('ThingyClient', () => {
  let client: ThingyClient;

  beforeEach(() => {
    client = new ThingyClient();
  });

  afterEach(async () => {
    await client.disconnect();
  });

  describe('scan', () => {
    it('should discover Thingy devices', async () => {
      const devices = await client.scan(5);
      expect(devices).toBeInstanceOf(Array);
      if (devices.length > 0) {
        expect(devices[0]).toHaveProperty('address');
        expect(devices[0]).toHaveProperty('name');
        expect(devices[0]).toHaveProperty('rssi');
      }
    });

    it('should filter by RSSI threshold', async () => {
      const devices = await client.scan(5, -50);
      devices.forEach(device => {
        expect(device.rssi).toBeGreaterThanOrEqual(-50);
      });
    });
  });

  describe('connect', () => {
    it('should connect to a valid device', async () => {
      const devices = await client.scan(5);
      if (devices.length > 0) {
        const success = await client.connect(devices[0].address);
        expect(success).toBe(true);
        expect(client.isConnected).toBe(true);
      }
    });

    it('should timeout on invalid address', async () => {
      await expect(client.connect('AA:BB:CC:DD:EE:FF', 2))
        .rejects.toThrow('Connection timeout');
    });
  });

  describe('readTemperature', () => {
    it('should read temperature value', async () => {
      const devices = await client.scan(5);
      if (devices.length > 0) {
        await client.connect(devices[0].address);
        const temp = await client.readTemperature();
        expect(typeof temp).toBe('number');
        expect(temp).toBeGreaterThan(-40);
        expect(temp).toBeLessThan(85);
      }
    });

    it('should throw error when not connected', async () => {
      await expect(client.readTemperature())
        .rejects.toThrow('Not connected to device');
    });
  });
});
```

### 9.3 Integration Tests

```typescript
// tests/integration/sensors.test.ts

import { describe, it, expect } from 'vitest';
import { ThingyClient } from '../../src/client/ThingyClient';

describe('Sensor Integration Tests', () => {
  it('should read all environmental sensors', async () => {
    const client = new ThingyClient();
    const devices = await client.scan(10);

    if (devices.length === 0) {
      console.warn('No Thingy devices found - skipping integration tests');
      return;
    }

    await client.connect(devices[0].address);

    const temp = await client.readTemperature();
    const humidity = await client.readHumidity();
    const pressure = await client.readPressure();
    const airQuality = await client.readAirQuality();

    expect(temp).toBeDefined();
    expect(humidity).toBeDefined();
    expect(pressure).toBeDefined();
    expect(airQuality.co2).toBeDefined();
    expect(airQuality.tvoc).toBeDefined();

    await client.disconnect();
  }, 30000);  // 30 second timeout
});
```

---

## 10. Deployment & Configuration

### 10.1 Claude Desktop Configuration

```json
{
  "mcpServers": {
    "thingy52-nodejs": {
      "command": "node",
      "args": [
        "/absolute/path/to/thingy52-mcp-server/dist/index.js"
      ],
      "env": {
        "NODE_ENV": "production",
        "LOG_LEVEL": "info",
        "AUTO_RECONNECT": "true",
        "MAX_RECONNECT_ATTEMPTS": "10"
      }
    }
  }
}
```

### 10.2 Environment Configuration

```bash
# .env

# Server Configuration
NODE_ENV=production
SERVER_NAME=Nordic Thingy:52
SERVER_VERSION=1.0.0
LOG_LEVEL=info

# Connection Configuration
AUTO_RECONNECT=true
MAX_RECONNECT_ATTEMPTS=10
INITIAL_RETRY_DELAY=1000
MAX_RETRY_DELAY=30000

# Performance Configuration
SENSOR_POLL_INTERVAL=1000
MOTION_PROCESSING_FREQ=100
CONNECTION_TIMEOUT=30000

# Feature Flags
ENABLE_MICROPHONE=true
ENABLE_AUDIO_RECORDING=true
ENABLE_REAL_TIME_STREAMING=true
```

### 10.3 Build & Run Commands

```json
{
  "scripts": {
    "dev": "tsx src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest",
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src --ext .ts",
    "lint:fix": "eslint src --ext .ts --fix",
    "format": "prettier --write \"src/**/*.ts\"",
    "typecheck": "tsc --noEmit"
  }
}
```

### 10.4 Production Deployment

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Run tests
npm run test

# Start production server
npm start
```

---

## Summary

This comprehensive plan provides a complete roadmap for building a **feature-rich Node.js TypeScript MCP server** for the Nordic Thingy:52 that:

✅ **Includes all 25 Python features** (device management, environmental sensors, motion, LED, sound)
✅ **Adds 22 new advanced features** (microphone streaming, audio recording, advanced motion, event subscriptions)
✅ **Provides full TypeScript type safety** with Zod validation
✅ **Implements event-driven architecture** for real-time sensor streaming
✅ **Includes auto-reconnect** with exponential backoff
✅ **Offers 47 total MCP tools** for comprehensive device control
✅ **Provides production-ready reliability** with error handling and testing

**Next Steps**: Begin Phase 1 implementation with project setup and foundational tools!
