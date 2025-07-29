# Balloon Risk Game: Behavioral Data Points and Trait Inference

## 1. Highly Granular Behavioral Data Points

### Per Session
- Session start and end timestamps
- Total number of balloons presented
- Total number of balloons popped
- Total number of balloons cashed out
- Total earnings (virtual money)
- Session duration
- Device/browser info (for context)

### Per Balloon
- Balloon color/type/variant
- Balloon index/order in session
- Balloon start timestamp
- Balloon end timestamp
- Outcome (popped/cashed out)
- Number of pumps for this balloon
- Maximum pumps reached
- Time to first pump
- Time to last pump
- Time between pumps (list of intervals)
- Time from last pump to cash out or pop
- Whether the balloon was pumped to a new personal max
- Whether the balloon was pumped more/less than previous balloons

### Per Pump Action
- Pump timestamp
- Pump number (nth pump for this balloon)
- Time since previous pump
- Balloon size at pump
- Balloon color at pump
- Current earnings for this balloon
- Current total earnings
- User’s reaction time (from balloon appearance to first pump)
- User’s reaction time (from previous pump to this pump)
- Whether the pump was rapid or hesitant (based on interval)

### Per Cash Out Action
- Cash out timestamp
- Number of pumps before cash out
- Time since last pump
- Earnings collected for this balloon
- Cumulative earnings at cash out
- Whether user hesitated before cashing out (long pause before action)
- Whether user cashed out after a risky sequence (e.g., after several rapid pumps)

### Per Pop Event
- Pop timestamp
- Number of pumps at pop
- Time since last pump
- Earnings lost (if any)
- Whether user showed risk escalation (e.g., more pumps than average)
- Whether pop followed a pattern (e.g., after a color change)

### Behavioral Patterns & Meta-Metrics
- Average pumps per balloon
- Standard deviation of pumps per balloon
- Average time per balloon
- Average time between pumps
- Change in pumping speed over session (learning/adaptation)
- Change in risk-taking over session (e.g., more/less pumps as session progresses)
- Response to negative feedback (change in behavior after a pop)
- Response to positive feedback (change in behavior after a successful cash out)
- Consistency of pumping strategy (variance in pump intervals)
- Pattern recognition (e.g., does user adjust strategy based on balloon color or previous outcomes)

### Other Contextual Data
- User’s focus/blur events (did they switch tabs?)
- Any interruptions or pauses
- Mouse movement or hover data (if feasible)
- Any error or unexpected behavior events

## 2. Inferred Cognitive, Socio-Emotional, and Behavioral Traits

### Cognitive Traits
- Risk Assessment & Pattern Recognition
- Decision-Making Style
- Learning & Adaptivity
- Attention & Focus
- Working Memory

### Socio-Emotional Traits
- Risk Tolerance
- Resilience & Emotional Regulation
- Reward Sensitivity
- Patience & Impulsivity
- Confidence

### Behavioral Traits
- Persistence
- Adaptability
- Consistency
- Cautiousness vs. Boldness
- Strategic Planning

### Meta-Traits (Composite)
- Self-Control
- Stress Response
- Motivation & Engagement

## 3. Categorization into Broad, Bi-Directional Dimensions

1. Risk Tolerance vs. Risk Aversion
2. Deliberation vs. Impulsivity
3. Persistence vs. Resignation
4. Adaptability vs. Rigidity
5. Consistency vs. Variability
6. Patience vs. Urgency
7. Confidence vs. Cautiousness
8. Emotional Regulation vs. Reactivity
9. Engagement vs. Distraction
10. Strategic Planning vs. Randomness

---

This file serves as a template for the remaining games. The following files will be created for each game, following this structure, but tailored to the specific mechanics and psychometric opportunities of each game.
