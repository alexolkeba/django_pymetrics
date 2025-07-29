# Tower of Hanoi Game: Behavioral Data Points and Trait Inference

## 1. Highly Granular Behavioral Data Points

### Per Session
- Session start and end timestamps
- Total number of puzzles presented
- Total puzzles solved
- Total moves made
- Session duration
- Device/browser info

### Per Puzzle
- Puzzle index/order in session
- Number of disks
- Minimum moves required
- User’s total moves
- Puzzle start timestamp
- Puzzle end timestamp
- Time to solve puzzle
- Number of errors (illegal moves)
- Number of restarts (if allowed)
- Whether puzzle was solved optimally

### Per Move Action
- Move timestamp
- Disk moved
- From peg
- To peg
- Time since previous move
- Correction/undo events
- Hesitation before move (long pauses)

### Behavioral Patterns & Meta-Metrics
- Average moves per puzzle
- Standard deviation of moves per puzzle
- Average time per puzzle
- Change in moves/time over session
- Error patterns (e.g., repeated illegal moves)
- Consistency of move speed
- Response to errors (change in behavior after illegal move)
- Planning vs. trial-and-error patterns

### Other Contextual Data
- User’s focus/blur events
- Interruptions or pauses
- Mouse movement or hover data (if feasible)
- Any error or unexpected behavior events

## 2. Inferred Cognitive, Socio-Emotional, and Behavioral Traits

### Cognitive Traits
- Planning & Problem Solving
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

1. Planning Skill (high vs. low)
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

This file documents the behavioral data schema, trait inference, and trait dimension mapping for the Tower of Hanoi game. Use this as a guide for data collection and psychometric analysis.
