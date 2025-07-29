# Memory Cards Game: Behavioral Data Points and Trait Inference

## 1. Highly Granular Behavioral Data Points

### Per Session
- Session start and end timestamps
- Total number of card pairs presented
- Total matches found
- Total errors (incorrect matches)
- Session duration
- Device/browser info

### Per Round/Turn
- Turn index/order in session
- Cards selected (IDs/positions)
- Time of first card selection
- Time of second card selection
- Time to complete turn
- Whether match was correct or incorrect
- Number of attempts per pair
- Time between selections
- Correction/change of selection (if allowed)
- Hesitation before selection (long pauses)

### Per Action
- Action timestamp
- Card selected
- Position in grid
- Time since previous action
- Correction/backtrack events

### Behavioral Patterns & Meta-Metrics
- Accuracy rate (matches found vs. attempts)
- Average time per turn
- Change in accuracy/time over session
- Error patterns (e.g., repeated mistakes on same pairs)
- Consistency of selection speed
- Response to errors (change in behavior after incorrect match)
- Biases (e.g., tendency to select certain positions)

### Other Contextual Data
- User’s focus/blur events
- Interruptions or pauses
- Mouse movement or hover data (if feasible)
- Any error or unexpected behavior events

## 2. Inferred Cognitive, Socio-Emotional, and Behavioral Traits

### Cognitive Traits
- Visual Working Memory
- Attention & Focus
- Learning & Adaptivity
- Error Monitoring
- Sequential Processing

### Socio-Emotional Traits
- Frustration Tolerance
- Resilience (response to errors)
- Confidence
- Motivation

### Behavioral Traits
- Persistence
- Consistency
- Adaptability
- Patience

### Meta-Traits (Composite)
- Self-Control
- Stress Response
- Engagement

## 3. Categorization into Broad, Bi-Directional Dimensions

1. Visual Memory Capacity (high vs. low)
2. Attention vs. Distraction
3. Persistence vs. Resignation
4. Adaptability vs. Rigidity
5. Consistency vs. Variability
6. Patience vs. Urgency
7. Confidence vs. Hesitation
8. Emotional Regulation vs. Reactivity
9. Engagement vs. Distraction
10. Error Monitoring vs. Carelessness

---

This file documents the behavioral data schema, trait inference, and trait dimension mapping for the Memory Cards game. Use this as a guide for data collection and psychometric analysis.
