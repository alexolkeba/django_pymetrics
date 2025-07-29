# Emotional Faces Game: Behavioral Data Points and Trait Inference

## 1. Highly Granular Behavioral Data Points

### Per Session
- Session start and end timestamps
- Total number of faces presented
- Total correct identifications
- Total incorrect identifications
- Session duration
- Device/browser info

### Per Face/Trial
- Face image ID
- Emotion displayed (ground truth)
- Trial index/order in session
- Time face appeared
- Time of user response
- Time to respond (reaction time)
- User’s selected emotion
- Whether response was correct or incorrect
- Confidence rating (if collected)
- Number of attempts (if retries allowed)
- Type of error (confusion between specific emotions)
- Whether user skipped or timed out

### Per Response Action
- Response timestamp
- Emotion selected
- Time since face appeared
- Correction/change of answer (if allowed)
- Hesitation before response (long pauses)

### Behavioral Patterns & Meta-Metrics
- Accuracy rate (overall, per emotion)
- Average reaction time (overall, per emotion)
- Error patterns (e.g., confusion matrix)
- Change in accuracy/reaction time over session
- Consistency of response speed
- Response to errors (change in behavior after incorrect response)
- Biases (e.g., tendency to mislabel certain emotions)

### Other Contextual Data
- User’s focus/blur events
- Interruptions or pauses
- Mouse movement or hover data (if feasible)
- Any error or unexpected behavior events

## 2. Inferred Cognitive, Socio-Emotional, and Behavioral Traits

### Cognitive Traits
- Emotion Recognition Ability
- Attention & Focus
- Learning & Adaptivity
- Decision-Making Speed
- Error Monitoring

### Socio-Emotional Traits
- Empathy
- Emotional Sensitivity
- Confidence
- Resilience (response to errors)
- Social Perception

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

1. Emotion Recognition Accuracy (high vs. low)
2. Attention vs. Distraction
3. Consistency vs. Variability
4. Adaptability vs. Rigidity
5. Patience vs. Urgency
6. Confidence vs. Hesitation
7. Emotional Sensitivity vs. Blunting
8. Engagement vs. Distraction
9. Error Monitoring vs. Carelessness
10. Bias Awareness vs. Unawareness

---

This file documents the behavioral data schema, trait inference, and trait dimension mapping for the Emotional Faces game. Use this as a guide for data collection and psychometric analysis.
