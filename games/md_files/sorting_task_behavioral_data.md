# Sorting Task Game: Behavioral Data Points and Trait Inference

## 1. Highly Granular Behavioral Data Points

### Per Session
- Session start and end timestamps
- Total number of sorting trials
- Total correct sorts
- Total incorrect sorts
- Session duration
- Device/browser info

### Per Trial
- Trial index/order in session
- Items to be sorted (list/IDs)
- Correct order (ground truth)
- User’s sorted order
- Time trial started
- Time trial ended
- Time to complete sort
- Number of moves/changes
- Number of errors (misplaced items)
- Type of error (specific items misplaced)
- Whether user requested a hint (if allowed)
- Whether user retried trial (if allowed)

### Per Action
- Action timestamp
- Item moved
- From/to position
- Time since previous action
- Correction/change of move
- Hesitation before move (long pauses)

### Behavioral Patterns & Meta-Metrics
- Accuracy rate (overall, per item)
- Average time per trial
- Change in accuracy/time over session
- Error patterns (e.g., repeated mistakes on same items)
- Consistency of sorting speed
- Response to errors (change in behavior after incorrect sort)
- Biases (e.g., tendency to misplace certain items)

### Other Contextual Data
- User’s focus/blur events
- Interruptions or pauses
- Mouse movement or hover data (if feasible)
- Any error or unexpected behavior events

## 2. Inferred Cognitive, Socio-Emotional, and Behavioral Traits

### Cognitive Traits
- Sequencing Ability
- Attention & Focus
- Learning & Adaptivity
- Error Monitoring
- Planning & Organization

### Socio-Emotional Traits
- Confidence
- Resilience (response to errors)
- Motivation

### Behavioral Traits
- Consistency
- Adaptability
- Patience
- Bias Awareness

### Meta-Traits (Composite)
- Self-Control
- Stress Response
- Engagement

## 3. Categorization into Broad, Bi-Directional Dimensions

1. Sequencing Skill (high vs. low)
2. Attention vs. Distraction
3. Consistency vs. Variability
4. Adaptability vs. Rigidity
5. Patience vs. Urgency
6. Confidence vs. Hesitation
7. Planning vs. Randomness
8. Engagement vs. Distraction
9. Error Monitoring vs. Carelessness
10. Bias Awareness vs. Unawareness

---

This file documents the behavioral data schema, trait inference, and trait dimension mapping for the Sorting Task game. Use this as a guide for data collection and psychometric analysis.
