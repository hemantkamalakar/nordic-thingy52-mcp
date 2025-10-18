# Automation Rules Engine

## Overview

The Automation Rules Engine is a feature that enables conditional automation of Thingy:52 device actions based on sensor readings, time schedules, and external events. It allows users to create sophisticated IoT workflows through natural language or programmatic rule definitions.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Automation Engine Core                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Rule Manager │  │   Scheduler  │  │Event Emitter │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│  ┌──────▼──────────────────▼──────────────────▼───────┐    │
│  │              Rule Execution Engine                  │    │
│  └──────┬─────────────────────────────────────────────┘    │
│         │                                                    │
│  ┌──────▼───────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Condition   │  │    Action    │  │   Context    │     │
│  │  Evaluator   │  │   Executor   │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                               │
└───────────────────┬───────────────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │  Thingy BLE Client    │
        │  (Sensors & Actuators)│
        └───────────────────────┘
```

### 1. Rule Manager

**Responsibilities:**
- Create, read, update, delete (CRUD) automation rules
- Validate rule syntax and logic
- Store rules in persistent storage (JSON/SQLite)
- Manage rule priorities and conflicts

**Key Classes:**
```python
class RuleManager:
    def add_rule(self, rule: Rule) -> str
    def remove_rule(self, rule_id: str) -> bool
    def update_rule(self, rule_id: str, rule: Rule) -> bool
    def get_rule(self, rule_id: str) -> Optional[Rule]
    def list_rules(self, filters: dict) -> List[Rule]
    def enable_rule(self, rule_id: str) -> bool
    def disable_rule(self, rule_id: str) -> bool
```

### 2. Scheduler

**Responsibilities:**
- Manage time-based rule execution
- Handle cron-like schedules
- Manage polling intervals for sensor monitoring
- Coordinate rule evaluation timing

**Key Classes:**
```python
class Scheduler:
    def schedule_rule(self, rule: Rule) -> None
    def unschedule_rule(self, rule_id: str) -> None
    def set_polling_interval(self, sensor: str, interval: float) -> None
    async def run(self) -> None  # Main event loop
```

### 3. Event Emitter

**Responsibilities:**
- Emit events when sensor values change
- Publish system events (connection, disconnection, errors)
- Support event-driven rule triggers
- Implement pub-sub pattern for loose coupling

**Key Classes:**
```python
class EventEmitter:
    def emit(self, event: Event) -> None
    def subscribe(self, event_type: str, callback: Callable) -> str
    def unsubscribe(self, subscription_id: str) -> None
```

### 4. Rule Execution Engine

**Responsibilities:**
- Execute rules when triggered
- Manage rule execution context and state
- Handle async execution of conditions and actions
- Implement execution strategies (sequential, parallel)
- Track execution history and statistics

**Key Classes:**
```python
class ExecutionEngine:
    async def evaluate_rule(self, rule: Rule, context: Context) -> bool
    async def execute_rule(self, rule: Rule, context: Context) -> ExecutionResult
    def get_execution_history(self, rule_id: str) -> List[ExecutionRecord]
```

### 5. Condition Evaluator

**Responsibilities:**
- Evaluate rule conditions against current state
- Support complex logical expressions (AND, OR, NOT)
- Compare sensor values with thresholds
- Evaluate time-based conditions
- Support custom condition functions

**Supported Condition Types:**
- **Comparison:** `temperature > 25`, `humidity < 60`
- **Range:** `temperature between 20 and 25`
- **Change Detection:** `temperature changed by > 5 in 10 minutes`
- **Time-based:** `time is 08:00`, `day is Monday`
- **Composite:** `(temperature > 25 AND humidity > 70) OR co2 > 1000`
- **Duration:** `temperature > 25 for 5 minutes`

### 6. Action Executor

**Responsibilities:**
- Execute actions when conditions are met
- Support multiple action types
- Handle action failures and retries
- Log action execution

**Supported Action Types:**
- **Device Control:** Set LED color, play sound
- **Notifications:** Log message, send webhook
- **Data Logging:** Record sensor value to file
- **Rule Control:** Enable/disable other rules
- **Chaining:** Trigger another rule

### 7. Context Manager

**Responsibilities:**
- Maintain execution context for rules
- Store historical sensor data
- Track rule state and variables
- Provide data for condition evaluation

## Data Models

### Rule Definition

```python
class Rule(BaseModel):
    """A rule defines when and what actions to execute."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Human-readable rule name")
    description: Optional[str] = None
    enabled: bool = Field(True, description="Whether the rule is active")
    priority: int = Field(0, description="Rule priority (higher = earlier execution)")

    # Trigger configuration
    trigger: Trigger = Field(..., description="What triggers this rule")

    # Conditions
    conditions: List[Condition] = Field(default_factory=list, description="Conditions that must be met")

    # Actions
    actions: List[Action] = Field(..., description="Actions to execute when conditions are met")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_executed: Optional[datetime] = None
    execution_count: int = 0

    # Advanced options
    cooldown_seconds: int = Field(0, description="Minimum time between executions")
    max_executions: Optional[int] = Field(None, description="Maximum number of executions")
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class Trigger(BaseModel):
    """Defines what triggers a rule evaluation."""

    type: str = Field(..., description="Trigger type: 'sensor', 'time', 'event', 'manual'")
    config: dict = Field(..., description="Trigger-specific configuration")

    # Examples:
    # Sensor: {"type": "sensor", "config": {"sensor": "temperature", "interval": 60}}
    # Time: {"type": "time", "config": {"cron": "0 8 * * *"}}
    # Event: {"type": "event", "config": {"event": "device_disconnected"}}


class Condition(BaseModel):
    """A condition that must be satisfied for the rule to execute."""

    type: str = Field(..., description="Condition type: 'comparison', 'range', 'time', 'composite', 'duration'")
    config: dict = Field(..., description="Condition-specific configuration")
    operator: Optional[str] = Field(None, description="Logical operator for composite conditions: 'AND', 'OR', 'NOT'")

    # Examples:
    # Comparison: {"type": "comparison", "config": {"sensor": "temperature", "operator": ">", "value": 25}}
    # Range: {"type": "range", "config": {"sensor": "co2", "min": 400, "max": 1000}}
    # Time: {"type": "time", "config": {"time": "08:00", "days": ["Monday", "Tuesday"]}}
    # Duration: {"type": "duration", "config": {"condition": {...}, "duration_seconds": 300}}


class Action(BaseModel):
    """An action to execute when conditions are met."""

    type: str = Field(..., description="Action type: 'led', 'sound', 'log', 'webhook', 'rule_control'")
    config: dict = Field(..., description="Action-specific configuration")
    retry_on_failure: bool = Field(False, description="Whether to retry on failure")
    max_retries: int = Field(3, description="Maximum retry attempts")

    # Examples:
    # LED: {"type": "led", "config": {"color": "red", "intensity": 100}}
    # Sound: {"type": "sound", "config": {"sound_id": 1}}
    # Log: {"type": "log", "config": {"message": "Temperature alert!", "level": "warning"}}
    # Webhook: {"type": "webhook", "config": {"url": "https://...", "method": "POST", "data": {...}}}


class ExecutionResult(BaseModel):
    """Result of a rule execution."""

    rule_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool
    conditions_met: bool
    actions_executed: List[str]
    errors: List[str] = Field(default_factory=list)
    execution_time_ms: float
```

## Use Cases & Examples

### 1. Air Quality Monitoring with Alerts

**Natural Language:**
"If CO2 exceeds 1000 ppm for more than 5 minutes, turn the LED red and play alert sound."

**Rule Definition:**
```python
Rule(
    name="High CO2 Alert",
    description="Alert when CO2 levels are too high",
    trigger=Trigger(
        type="sensor",
        config={"sensor": "co2", "interval": 30}
    ),
    conditions=[
        Condition(
            type="duration",
            config={
                "condition": {
                    "type": "comparison",
                    "config": {"sensor": "co2", "operator": ">", "value": 1000}
                },
                "duration_seconds": 300  # 5 minutes
            }
        )
    ],
    actions=[
        Action(type="led", config={"color": "red", "intensity": 100}),
        Action(type="sound", config={"sound_id": 2}),
        Action(type="log", config={"message": "CO2 alert: {co2} ppm", "level": "warning"})
    ],
    cooldown_seconds=600  # Don't re-alert for 10 minutes
)
```

### 2. Meeting Room Occupancy Status

**Natural Language:**
"During work hours (9 AM - 5 PM), set LED to green if CO2 < 800 ppm (room available), yellow if 800-1200 ppm (occupied), red if > 1200 ppm (ventilation needed)."

**Rule Definition:**
```python
# Rule 1: Available
Rule(
    name="Room Available",
    trigger=Trigger(type="sensor", config={"sensor": "co2", "interval": 60}),
    conditions=[
        Condition(type="time", config={"time_range": ["09:00", "17:00"]}),
        Condition(type="comparison", config={"sensor": "co2", "operator": "<", "value": 800})
    ],
    actions=[Action(type="led", config={"color": "green", "intensity": 50})],
    priority=1
)

# Rule 2: Occupied
Rule(
    name="Room Occupied",
    trigger=Trigger(type="sensor", config={"sensor": "co2", "interval": 60}),
    conditions=[
        Condition(type="time", config={"time_range": ["09:00", "17:00"]}),
        Condition(type="range", config={"sensor": "co2", "min": 800, "max": 1200})
    ],
    actions=[Action(type="led", config={"color": "yellow", "intensity": 50})],
    priority=2
)

# Rule 3: Needs Ventilation
Rule(
    name="Room Needs Ventilation",
    trigger=Trigger(type="sensor", config={"sensor": "co2", "interval": 60}),
    conditions=[
        Condition(type="time", config={"time_range": ["09:00", "17:00"]}),
        Condition(type="comparison", config={"sensor": "co2", "operator": ">", "value": 1200})
    ],
    actions=[Action(type="led", config={"color": "red", "intensity": 100})],
    priority=3
)
```

### 3. Cold Chain Monitoring

**Natural Language:**
"Log temperature every minute. If temperature goes above 5°C or below -20°C, immediately alert and record event."

**Rule Definition:**
```python
# Rule 1: Data Logging
Rule(
    name="Temperature Logger",
    trigger=Trigger(type="time", config={"cron": "* * * * *"}),  # Every minute
    conditions=[],  # Always execute
    actions=[
        Action(
            type="log",
            config={
                "file": "temperature_log.csv",
                "format": "{timestamp},{temperature}",
                "append": True
            }
        )
    ]
)

# Rule 2: Out of Range Alert
Rule(
    name="Temperature Out of Range",
    trigger=Trigger(type="sensor", config={"sensor": "temperature", "interval": 10}),
    conditions=[
        Condition(
            type="composite",
            operator="OR",
            config={
                "conditions": [
                    {"type": "comparison", "config": {"sensor": "temperature", "operator": ">", "value": 5}},
                    {"type": "comparison", "config": {"sensor": "temperature", "operator": "<", "value": -20}}
                ]
            }
        )
    ],
    actions=[
        Action(type="led", config={"color": "red", "intensity": 100}),
        Action(type="sound", config={"sound_id": 3}),
        Action(
            type="webhook",
            config={
                "url": "https://api.example.com/alerts",
                "method": "POST",
                "data": {"alert": "Temperature out of range", "value": "{temperature}"}
            },
            retry_on_failure=True
        ),
        Action(
            type="log",
            config={
                "file": "alerts.log",
                "message": "ALERT: Temperature {temperature}°C at {timestamp}",
                "level": "critical"
            }
        )
    ],
    cooldown_seconds=300  # Alert every 5 minutes if condition persists
)
```

### 4. Fall Detection for Elderly Care

**Natural Language:**
"If accelerometer detects sudden deceleration (fall pattern), immediately sound alarm and send alert."

**Rule Definition:**
```python
Rule(
    name="Fall Detection",
    trigger=Trigger(type="sensor", config={"sensor": "accelerometer", "interval": 0.1}),  # 10 Hz
    conditions=[
        Condition(
            type="custom",
            config={
                "function": "detect_fall_pattern",
                "params": {
                    "threshold_g": 2.5,
                    "impact_duration_ms": 100
                }
            }
        )
    ],
    actions=[
        Action(type="sound", config={"sound_id": 8}),  # Emergency sound
        Action(type="led", config={"color": "red", "mode": "flash"}),
        Action(
            type="webhook",
            config={
                "url": "https://emergency.example.com/fall-alert",
                "method": "POST",
                "data": {
                    "alert_type": "fall_detected",
                    "device_id": "{device_address}",
                    "timestamp": "{timestamp}",
                    "location": "{location}"
                }
            },
            retry_on_failure=True,
            max_retries=5
        ),
        Action(
            type="sms",
            config={
                "recipients": ["+1234567890"],
                "message": "Fall detected! Time: {timestamp}"
            }
        )
    ],
    cooldown_seconds=60  # Prevent multiple alerts for same fall
)
```

### 5. Comfort Zone Tracking

**Natural Language:**
"Monitor comfort score based on temperature (20-24°C), humidity (40-60%), and CO2 (<800 ppm). Display status via LED color."

**Rule Definition:**
```python
# Custom function to calculate comfort score
def calculate_comfort_score(temp, humidity, co2):
    score = 100
    if not (20 <= temp <= 24):
        score -= abs(temp - 22) * 5
    if not (40 <= humidity <= 60):
        score -= abs(humidity - 50) * 2
    if co2 > 800:
        score -= (co2 - 800) / 10
    return max(0, min(100, score))

Rule(
    name="Comfort Zone Monitor",
    trigger=Trigger(type="sensor", config={"sensors": ["temperature", "humidity", "co2"], "interval": 60}),
    conditions=[],  # Always execute
    actions=[
        Action(
            type="custom",
            config={
                "function": "update_comfort_display",
                "params": {
                    "score": "{comfort_score}",
                    "led_mapping": {
                        "excellent": {"color": "green", "threshold": 80},
                        "good": {"color": "blue", "threshold": 60},
                        "fair": {"color": "yellow", "threshold": 40},
                        "poor": {"color": "red", "threshold": 0}
                    }
                }
            }
        ),
        Action(
            type="log",
            config={
                "file": "comfort_log.csv",
                "format": "{timestamp},{temperature},{humidity},{co2},{comfort_score}"
            }
        )
    ]
)
```

## MCP Tools for Automation Engine

```python
@mcp.tool()
async def create_automation_rule(
    name: str,
    description: str,
    trigger: dict,
    conditions: List[dict],
    actions: List[dict],
    **options
) -> dict:
    """Create a new automation rule."""

@mcp.tool()
async def list_automation_rules(enabled_only: bool = False) -> List[dict]:
    """List all automation rules."""

@mcp.tool()
async def get_automation_rule(rule_id: str) -> dict:
    """Get details of a specific rule."""

@mcp.tool()
async def update_automation_rule(rule_id: str, updates: dict) -> dict:
    """Update an existing rule."""

@mcp.tool()
async def delete_automation_rule(rule_id: str) -> dict:
    """Delete a rule."""

@mcp.tool()
async def enable_automation_rule(rule_id: str) -> dict:
    """Enable a rule."""

@mcp.tool()
async def disable_automation_rule(rule_id: str) -> dict:
    """Disable a rule."""

@mcp.tool()
async def test_automation_rule(rule_id: str, mock_data: Optional[dict] = None) -> dict:
    """Test a rule without actually executing actions."""

@mcp.tool()
async def get_rule_execution_history(rule_id: str, limit: int = 100) -> List[dict]:
    """Get execution history for a rule."""

@mcp.tool()
async def get_automation_statistics() -> dict:
    """Get overall statistics about automation engine."""
```

## Implementation Phases

### Phase 1: Core Foundation (Week 1-2)
- Rule data models and validation
- Rule Manager with CRUD operations
- Basic Condition Evaluator (comparison, range)
- Basic Action Executor (LED, sound, log)
- Persistent storage (JSON files)

### Phase 2: Scheduling & Events (Week 3-4)
- Scheduler implementation
- Time-based triggers
- Event emitter & pub-sub system
- Sensor polling with configurable intervals

### Phase 3: Advanced Conditions (Week 5-6)
- Duration-based conditions
- Change detection
- Composite conditions (AND, OR, NOT)
- Custom condition functions
- Historical data tracking

### Phase 4: Advanced Actions (Week 7-8)
- Webhook actions
- Rule chaining
- Action retry logic
- Custom action functions
- Email/SMS notifications (via external APIs)

### Phase 5: Monitoring & Management (Week 9-10)
- Execution history tracking
- Statistics and analytics
- Rule testing/simulation
- Web dashboard (optional)
- Performance optimization

## Configuration

```python
# config/automation.yaml
automation:
  enabled: true
  storage:
    type: "sqlite"  # or "json"
    path: "data/rules.db"

  scheduler:
    polling_interval: 1.0  # seconds
    max_concurrent_rules: 10

  execution:
    timeout_seconds: 30
    retry_failed_actions: true
    max_action_retries: 3

  history:
    enabled: true
    retention_days: 30
    max_records_per_rule: 1000

  sensors:
    default_poll_interval: 60
    poll_intervals:
      temperature: 30
      humidity: 30
      co2: 60
      motion: 0.1
```

## Security Considerations

1. **Rule Validation:** Validate all rule definitions to prevent malicious code execution
2. **Action Sandboxing:** Execute custom actions in sandboxed environment
3. **Webhook Security:** Validate webhook URLs, support authentication
4. **Rate Limiting:** Prevent rule execution floods
5. **Access Control:** Implement permissions for rule management (future)

## Performance Considerations

1. **Efficient Polling:** Use separate threads/tasks for different sensors
2. **Lazy Evaluation:** Only evaluate conditions when triggers fire
3. **Caching:** Cache sensor readings to avoid redundant BLE operations
4. **Async Execution:** Use asyncio for non-blocking rule execution
5. **Database Indexing:** Index rule IDs and timestamps in storage

## Testing Strategy

1. **Unit Tests:** Test each component in isolation
2. **Integration Tests:** Test rule execution end-to-end
3. **Performance Tests:** Measure execution latency and throughput
4. **Stress Tests:** Test with many concurrent rules
5. **Mock Hardware:** Test without physical Thingy:52 device

## Future Enhancements

1. **Machine Learning:** Predictive rules based on historical patterns
2. **Cloud Integration:** Sync rules and data to cloud
3. **Multi-Device:** Support multiple Thingy:52 devices
4. **Visual Editor:** GUI for rule creation
5. **Rule Templates:** Pre-built rules for common use cases
6. **Geofencing:** Location-based triggers
7. **Device Collaboration:** Rules spanning multiple devices
