# Behavioral Data Point and Trait Analysis

This document provides a comprehensive analysis of the behavioral data points collected from the 23 games in this project. For each game, it outlines the specific data points captured, the cognitive and behavioral traits inferred from these points, and the bi-directional dimensions used for categorization.

### Executive Summary

This document provides a detailed analysis for **23 games**. Across these games, we have defined:

*   **136 Unique Behavioral Data Points:** These are the raw, objective metrics captured during gameplay (e.g., reaction time, choice patterns, accuracy).
*   **98 Inferred Behavioral Traits:** These are the psychological constructs we derive from the data points (e.g., Risk-Taking Propensity, Working Memory Capacity, Selective Attention).
*   **86 Bi-Directional Dimensions:** These provide a spectrum for profiling, allowing individuals to be placed on a continuum for each trait (e.g., Risk-Seeking <-> Risk-Averse, Focused <-> Distractible).

The goal of this framework is to build a multi-faceted, data-driven psychological profile from observable in-game behavior. By collecting over **3,500 granular data points** from a single player across all games, the system can discern subtle patterns and nuances in human behavior that are imperceptible to simpler assessment methods. 

## Game 1: Arrows Game (Flanker Task)

**1. Behavioral Data Points:**

*   **Reaction Time (RT):** The time taken to respond to the target arrow in each trial, measured in milliseconds.
*   **Accuracy:** Whether the response was correct or incorrect for each trial.
*   **Condition Type:** Each trial is one of three types:
    *   **Congruent:** Flanker arrows point in the same direction as the target (e.g., >>>>>).
    *   **Incongruent:** Flanker arrows point in the opposite direction (e.g., >><>>).
    *   **Neutral:** Flankers are non-arrow symbols (e.g., ##>##).
*   **Flanker Effect:** The difference in reaction time between incongruent and congruent trials (RT_incongruent - RT_congruent). This is the primary measure of inhibitory control.
*   **Error Rate by Condition:** The percentage of errors made in each of the three conditions.
*   **Event Log:** A detailed record of each trial, including the condition, the user's response, correctness, and reaction time.

**2. Inferred Behavioral Traits:**

*   **Selective Attention:** The ability to focus on relevant stimuli (the central arrow) while ignoring distracting information (the flanker arrows).
*   **Response Inhibition (Cognitive Control):** The core trait measured by the Flanker Effect. It is the ability to suppress a prepotent but incorrect response. A large Flanker Effect indicates greater difficulty in inhibiting the influence of the distracting flankers.
*   **Processing Speed:** The baseline speed of responding, often measured by the reaction time in the neutral or congruent conditions.
*   **Performance Under Conflict:** How well an individual can maintain accuracy and speed when faced with conflicting information.

**3. Bi-Directional Dimensions:**

*   **High Cognitive Control <-> Low Cognitive Control:** Directly measured by the size of the Flanker Effect. A smaller effect indicates more efficient response inhibition.
*   **Focused <-> Distractible:** A user with focused attention will have a smaller Flanker Effect and lower error rates in incongruent trials. A distractible user will be more influenced by the flankers.
*   **Accurate <-> Error-Prone:** Measured by the overall accuracy, especially the error rate in the high-conflict (incongruent) condition.
*   **Fast Processor <-> Slow Processor:** Measured by the average reaction time in the congruent or neutral conditions.

## Game 2: Attention Network Test (ANT)

**1. Behavioral Data Points:**

*   **Reaction Time (RT) and Accuracy:** Recorded for each trial.
*   **Cue Type:** Trials are preceded by one of four cue conditions:
    *   **No Cue:** A baseline condition.
    *   **Center Cue:** A cue appears at the center of the screen, indicating a target will soon appear, but not where.
    *   **Spatial Cue:** A cue appears at the location where the target will subsequently appear, directing attention to the correct location.
    *   **Double Cue:** Cues appear at both possible target locations.
*   **Flanker Condition:** The target arrow is either congruent (e.g., >>>>>) or incongruent (e.g., >><>>), similar to the basic Flanker Task.

**2. Inferred Behavioral Traits (Attention Networks):**

*   **Alerting:** The ability to achieve and maintain a state of high sensitivity to incoming stimuli. This is measured by the change in RT between 'No Cue' and 'Double Cue' trials. A positive alerting effect (faster RT with a double cue) indicates efficient arousal.
*   **Orienting:** The ability to select specific information from a variety of sensory inputs. This is measured by the change in RT between 'Center Cue' and 'Spatial Cue' trials. A positive orienting effect (faster RT with a spatial cue) shows efficient direction of attention.
*   **Executive Control (Conflict Resolution):** The ability to resolve conflict among responses. This is measured by the difference in RT between incongruent and congruent flanker trials (the Flanker Effect). This is the same core concept as in the standalone Arrows Game.

**3. Bi-Directional Dimensions:**

*   **Efficient <-> Inefficient Alerting:** Measured by the alerting effect size. Larger benefits from the double cue indicate more efficient alerting.
*   **Efficient <-> Inefficient Orienting:** Measured by the orienting effect size. Larger benefits from the spatial cue indicate more efficient shifting of attention.
*   **High <-> Low Executive Control:** Measured by the conflict (Flanker) effect size. A smaller difference between incongruent and congruent trials indicates better conflict resolution.

## Game 3: Balloon Risk (Adaptive Risk Challenge)

**1. Behavioral Data Points:**

*   **Pumps per Balloon:** The number of times the user pumps the balloon in each round.
*   **Explosion Points:** The round number (and pump number) at which each balloon was programmed to explode.
*   **Banked Earnings:** The amount of money successfully collected by the user in each round.
*   **Explosion Events:** A log of all rounds where the user pumped the balloon until it exploded, resulting in zero earnings for that round.
*   **Total Score:** The cumulative earnings across all rounds.
*   **Average Pumps (Adjusted):** The average number of pumps for all balloons that were successfully banked (i.e., not exploded). This is a key measure of the user's learned risk level.

**2. Inferred Behavioral Traits:**

*   **Risk-Taking Propensity:** The primary trait measured. It assesses the degree to which an individual is willing to take risks to achieve a greater reward.
*   **Learning from Feedback:** The game measures how users adjust their pumping behavior in response to balloon explosions (negative feedback). An adaptive player will likely pump less after an explosion.
*   **Impulsivity vs. Self-Control:** Pumping the balloon, especially after earning a significant amount in a round, requires overriding the safer impulse to bank the money.
*   **Probability Assessment:** While not explicit, players develop an intuitive sense of the risk of explosion as the balloon grows larger.

**3. Bi-Directional Dimensions:**

*   **Risk-Seeking <-> Risk-Averse:** Directly measured by the adjusted average number of pumps. A higher average indicates a more risk-seeking strategy.
*   **Adaptive <-> Reckless:** An adaptive player adjusts their risk-taking based on outcomes (e.g., pumping less after an explosion). A reckless player may continue to pump to the same high level regardless of negative feedback.
*   **Cautious <-> Audacious:** This dimension captures the user's general approach. A cautious player banks money early and often, while an audacious player consistently pushes the limits.

## Game 4: Cards Game (Strategic Investment Task)

**1. Behavioral Data Points:**

*   **Deck Choice:** The specific deck (A, B, C, or D) chosen in each of the 100 trials.
*   **Gain/Loss Schedule:** Each deck has a predefined pattern of rewards and punishments. Decks A and B offer high rewards but also high potential losses (Deck B is disadvantageous long-term). Decks C and D offer lower rewards but also lower losses (both are advantageous long-term).
*   **Net Score:** The running total of money won or lost throughout the game.
*   **Reaction Time:** The time taken to select a deck in each round.
*   **Deck Selection Frequency:** The total number of times each deck is chosen over the course of the game.
*   **Choice Progression:** The pattern of deck choices over time (e.g., shifting from disadvantageous to advantageous decks).
*   **Game Events:** A log of all `pick` events, including the deck chosen, gain, loss, and resulting score.
*   **Completion Status:** Whether the user completed all 100 trials or abandoned the game.

**2. Inferred Behavioral Traits:**

*   **Decision-Making Under Ambiguity:** The core trait measured. The game assesses the ability to identify patterns and make advantageous choices when faced with uncertain outcomes. Successful players learn to favor the decks with positive long-term prospects.
*   **Learning from Feedback:** The task measures how well individuals use the feedback (wins and losses) from their choices to guide future decisions. A shift away from the 'bad' decks (like Deck B) over time indicates effective learning.
*   **Executive Functioning:** This is a key component, as the player must weigh immediate gratification (high rewards from bad decks) against long-term, more optimal outcomes (consistent but smaller gains from good decks).
*   **Sensitivity to Punishment vs. Reward:** This trait is revealed by the player's reaction to large losses. A player highly sensitive to punishment will quickly avoid the decks that deliver large, unpredictable losses. A player more focused on reward may continue to chase the high payoffs from those same decks.
*   **Strategic Thinking:** The ability to develop a coherent strategy over time, such as consistently choosing from the low-risk, positive-outcome decks.

**3. Bi-Directional Dimensions:**

*   **Advantageous <-> Disadvantageous Decision-Making:** Measured by the net score and the proportion of choices from good decks vs. bad decks, especially in the latter half of the game.
*   **Future-Oriented <-> Present-Oriented:** A player who learns to choose the advantageous decks is demonstrating future-oriented thinking (delaying gratification for long-term gain). A player who keeps choosing from high-risk, high-reward decks is more present-oriented.
*   **Adaptive Learner <-> Inflexible:** Inferred from the change in deck selection patterns over time. A player who shifts their strategy based on outcomes is an adaptive learner.
*   **Risk-Averse <-> Risk-Seeking (in context of uncertainty):** While similar to the balloon game, this task assesses risk in the context of learning complex reward-punishment schedules. Choosing low-reward, low-loss decks (C, D) indicates a more risk-averse strategy in this context.

## Game 5: Digit Span (Working Memory Challenge)

**1. Behavioral Data Points:**

*   **Max Forward Span:** The longest sequence of digits the user correctly recalled in the original order.
*   **Max Backward Span:** The longest sequence of digits the user correctly recalled in reverse order.
*   **Trial-by-Trial Accuracy:** Whether the user's response was correct or incorrect for each sequence.
*   **Specific Errors:** The actual incorrect sequences submitted by the user.
*   **Progression:** How the span length changes over time for both forward and backward tasks.
*   **Incorrect Streak:** The number of consecutive incorrect answers at a given span length (the task ends after two).
*   **Event Log:** A detailed timeline including `trial_start`, `sequence_presented`, `response_submitted`, `span_increase`, and `task_switch` events.
*   **Completion Status:** Whether the user completed both the forward and backward tasks or abandoned the game.

**2. Inferred Behavioral Traits:**

*   **Working Memory Capacity:** The primary trait measured. This is the cognitive system for temporarily holding and manipulating information. The game assesses two key components:
    *   **Phonological Loop (Forward Span):** The forward task measures the capacity for simple auditory/verbal storage. It's about rehearsal and recall.
    *   **Central Executive (Backward Span):** The backward task is more demanding. It requires not just storing the digits but also mentally manipulating them (reversing the order), which is a core function of the central executive (attention, control, mental reorganization).
*   **Attention Control:** The ability to focus on the presented digits and ignore distractions is crucial for success.
*   **Cognitive Flexibility:** The ability to switch between the forward and backward recall tasks demonstrates mental adaptability.
*   **Information Processing:** The efficiency with which the user can encode the sequence, hold it, and then retrieve it for their response.

**3. Bi-Directional Dimensions:**

*   **High Working Memory Capacity <-> Low Working Memory Capacity:** Directly measured by the maximum spans achieved. A higher span indicates a greater capacity.
*   **Strong Central Executive Function <-> Weak Central Executive Function:** The difference between the backward and forward span is a key indicator. A significantly lower backward span compared to the forward span can suggest specific challenges with executive control and mental manipulation, as opposed to simple storage.
*   **Focused <-> Distractible:** Inferred from the consistency of performance. Frequent errors on relatively short spans might indicate lapses in attention.
*   **Mentally Flexible <-> Mentally Rigid:** Assessed by the user's ability to adapt to the rule change when switching from the forward to the backward task.

## Game 6: Cognitive Effort Task (Easy or Hard)

**1. Behavioral Data Points:**

*   **Choice Pattern:** The sequence of 'easy' or 'hard' choices across all 12 rounds.
*   **Frequency of Hard Choices:** The total number of times the user selected the high-effort, high-reward option.
*   **Hard Task Performance:**
    *   **Accuracy:** Whether the math problem was answered correctly.
    *   **Timeouts:** Whether the user failed to answer the math problem within the 5-second time limit.
*   **Total Score:** The cumulative points earned, reflecting both the choices made and the performance on the hard tasks.
*   **Event Log:** A detailed record of events including `choice_made` (with round number and choice), `hard_task_start`, and `hard_task_end` (with details on correctness and timeouts).
*   **Completion Status:** Whether the user completed all rounds or abandoned the game.

**2. Inferred Behavioral Traits:**

*   **Motivation & Willingness to Exert Effort:** The core trait measured. This assesses how much cognitive effort an individual is willing to expend to achieve a greater reward. Consistently choosing the 'hard' task indicates high motivation.
*   **Cost-Benefit Analysis:** The game requires a constant, implicit calculation of whether the potential for a higher reward justifies the increased mental effort and risk of failure associated with the hard task.
*   **Persistence & Frustration Tolerance:** Revealed by the user's choice pattern following a failure on a hard task (either an incorrect answer or a timeout). A persistent individual may continue to choose the hard option, while someone with lower frustration tolerance might switch to the 'easy' option.
*   **Metacognitive Judgment:** The user's implicit self-assessment of their ability to perform the hard task successfully. Choosing the hard task suggests confidence in one's arithmetic skills under time pressure.

**3. Bi-Directional Dimensions:**

*   **Driven <-> Apathetic:** A user who frequently chooses the hard task is considered more driven and motivated by rewards, while a user who exclusively chooses the easy task could be seen as more apathetic or effort-averse in this context.
*   **Effortful <-> Effort-Averse:** This dimension directly maps to the primary choice. It captures the preference for engaging in challenging tasks versus choosing the path of least resistance.
*   **Persistent <-> Easily Discouraged:** Measured by the user's choices after failing a 'hard' trial. Persistence is shown by re-selecting the hard task, while being easily discouraged is shown by switching to the easy task.
*   **Confident <-> Cautious:** This reflects the user's belief in their own abilities. Choosing the hard task is an act of confidence, while sticking to the guaranteed, smaller reward of the easy task is a more cautious approach.

## Game 7: Emotional Recognition Task (Faces Game)

This game is functionally similar to the *Facial Emotion Perception* task, assessing the user's ability to identify emotions from static images of faces. It uses a four-choice format (Happy, Sad, Angry, Surprised).

**1. Behavioral Data Points:**

*   **Accuracy (Hits):** The number and percentage of correctly identified emotions.
*   **Reaction Time:** The time taken to make a choice for each face.
*   **Score:** A performance metric calculated from both accuracy and reaction time.
*   **Choice Pattern:** The specific emotion chosen for each trial, which allows for creating a confusion matrix (e.g., how often 'surprised' is misidentified as 'angry').
*   **Event Log:** A detailed log of each trial, including the stimulus presented, the user's response, correctness, and reaction time.
*   **Completion Status:** Whether the user finished all 24 trials.

**2. Inferred Behavioral Traits:**

*   **Emotion Recognition:** The core trait, measuring the ability to accurately decode non-verbal emotional cues from faces.
*   **Social Cognition:** Taps into the broader ability to process and understand social information.
*   **Perceptual Processing Speed:** Reaction time provides a measure of how quickly an individual can process facial information and make a social judgment.
*   **Perceptual Bias:** Consistent error patterns (e.g., frequently mislabeling one emotion as another) can indicate underlying biases in emotion perception.

**3. Bi-Directional Dimensions:**

*   **High Emotional Acuity <-> Low Emotional Acuity:** Directly measured by accuracy and score. Higher scores reflect a more fine-tuned ability to identify emotions.
*   **Rapid Social Processor <-> Deliberate Social Processor:** Measured by reaction time. This dimension captures the speed of social-emotional judgment.
*   **Perceptually Unbiased <-> Prone to Perceptual Bias:** Inferred from analyzing patterns of incorrect answers. A lack of consistent error patterns suggests an unbiased perception.

## Game 8: Numerical Acuity Challenge (Magnitudes)

This game tests a user's **Number Sense** by asking them to judge which of two numbers is larger. The difficulty adapts based on their performance, homing in on the user's ability to make fine-grained numerical distinctions.

**1. Behavioral Data Points:**

*   **Reaction Time (RT):** The time taken to decide which number is larger.
*   **Accuracy:** Whether the choice was correct or incorrect.
*   **Numerical Ratio:** The ratio between the two numbers presented (e.g., 9 vs. 8 has a ratio of 1.125). This is the primary measure of difficulty.
*   **Weber Fraction (Estimated):** The smallest ratio at which the user can reliably distinguish between numbers, determined by the adaptive algorithm.
*   **Event Log:** A trial-by-trial record of the numbers presented, the user's choice, and the outcome.

**2. Inferred Behavioral Traits:**

*   **Number Sense (Numerical Acuity):** The core trait measured. This is the intuitive ability to perceive, process, and compare numerical quantities.
*   **Cognitive Processing Speed:** The baseline speed at which a user can make simple comparative judgments.
*   **Attentional Focus:** Consistency in performance, especially as the numerical ratios become more difficult to distinguish.

**3. Bi-Directional Dimensions:**

*   **High <-> Low Numerical Acuity:** Directly measured by the estimated Weber Fraction. A lower fraction indicates a more precise number sense.
*   **Quick <-> Deliberate Processor:** Inferred from the average reaction time on correct trials.
*   **Consistent <-> Inconsistent Performer:** Measured by the stability of performance. High variability in accuracy or RT may suggest fluctuating attention.

## Game 9: Rhythmic Precision Task (Keypresses)

This task is a continuous performance test that measures psychomotor speed, accuracy, and sustained attention. Users must press the correct keyboard key corresponding to a letter that appears on the screen as quickly as possible over a 60-second period.

**1. Behavioral Data Points:**

*   **Reaction Times:** A list of all individual reaction times for correct presses, measured in milliseconds.
*   **Average Reaction Time:** The mean of all correct reaction times.
*   **Accuracy (Hits vs. Misses):** The total number of correct key presses (hits) versus incorrect presses (misses).
*   **Score:** A composite metric based on the number of correct hits, with potential deductions for misses or slow responses.
*   **Reaction Time Variability:** The standard deviation of reaction times (can be calculated from the `reaction_times` array), indicating performance consistency.
*   **Event Log:** A detailed log of each trial, including the target letter, the key pressed, the reaction time, and whether it was a hit or miss.
*   **Completion Status:** Whether the user completed the full 60-second duration.

**2. Inferred Behavioral Traits:**

*   **Psychomotor Speed:** The core trait measured by the average reaction time. It reflects the speed of the entire perception-action cycle.
*   **Sustained Attention / Vigilance:** The ability to maintain focus and consistent performance over the duration of the task. This is inferred from accuracy and reaction time stability over time.
*   **Response Inhibition:** While not a primary focus, the number of 'misses' (pressing the wrong key) can indicate lapses in motor control or inhibition.
*   **Processing Speed:** A fundamental cognitive ability reflecting how quickly an individual can process incoming information and respond to it.
*   **Consistency:** Measured by the variability (standard deviation) in reaction times. Low variability suggests stable and consistent performance.

**3. Bi-Directional Dimensions:**

*   **Quick <-> Slow:** Directly measured by the average reaction time. This reflects the user's basic processing and motor speed.
*   **Accurate <-> Inaccurate:** Measured by the ratio of hits to misses. This dimension captures the user's ability to perform the task without making errors.
*   **Consistent <-> Variable:** Measured by the standard deviation of reaction times. A consistent performer will have a tight cluster of reaction times, while a variable performer will have a wide spread.
*   **Focused <-> Fatigued/Distractible:** Inferred by analyzing performance trends. A decline in accuracy or a significant increase in reaction time variability towards the end of the task could signal fatigue or a drop in sustained attention.

## Game 10: Perceptual Acuity Challenge (Lengths Game)

This is a classic psychophysical task designed to measure **perceptual sensitivity**. It uses an adaptive staircase procedure where the user must identify the longer of two lines. The difficulty automatically adjusts based on performance to find the user's **Just Noticeable Difference (JND)**—the smallest difference they can reliably detect.

**1. Behavioral Data Points:**

*   **Just Noticeable Difference (JND) / Final Difficulty:** The primary output of the game. It's the final percentage difference in line length that the user could consistently discriminate. A lower JND indicates higher perceptual acuity.
*   **Reaction Time:** The time taken to make a decision on each trial.
*   **Choice History & Difficulty Progression:** The log of correct/incorrect answers and the corresponding trial-by-trial adjustments to the difficulty level. This shows how the user's performance converges on their JND.
*   **Score & Streak:** Metrics reflecting consistent and accurate performance.
*   **Event Log:** A detailed record of each trial, including the specific line lengths presented, the user's choice, correctness, reaction time, and the difficulty level for that trial.
*   **Completion Status:** Whether the user completed all 40 rounds.

**2. Inferred Behavioral Traits:**

*   **Perceptual Acuity / Sensitivity:** The core trait being measured. This is the ability to discern fine-grained differences in visual stimuli.
*   **Visual-Spatial Judgment:** Reflects the ability to make accurate judgments about spatial properties (in this case, length).
*   **Decision-Making Under Uncertainty:** As the lines become very similar in length, the task requires making decisions with incomplete or ambiguous perceptual information.
*   **Cognitive-Perceptual Threshold:** The JND represents the boundary of the user's perceptual capabilities for this specific task.

**3. Bi-Directional Dimensions:**

*   **High Perceptual Acuity <-> Low Perceptual Acuity:** Directly and precisely measured by the final JND. A lower JND value signifies higher acuity.
*   **Decisive <-> Hesitant:** Measured by reaction times, especially on difficult trials (where the length difference is small). Longer reaction times may indicate more careful consideration or uncertainty.
*   **Consistent <-> Inconsistent (Perceptual Judgment):** Inferred from the stability of the difficulty parameter over the course of the game. A consistent performer will converge smoothly to a stable JND, while an inconsistent one will show large fluctuations in performance.
*   **Detail-Oriented <-> Gestalt-Focused:** This is a higher-level inference. A person with a very low JND is likely highly attuned to fine visual details, a characteristic of a detail-oriented cognitive style.

## Game 11: Cognitive Reflex Test (Letters Game)

This is an adaptive continuous performance task designed to measure processing speed, sustained attention, and cognitive flexibility under increasing cognitive load. Users must press the corresponding key for letters that appear randomly on the screen. The speed at which new letters appear increases as the user succeeds.

**1. Behavioral Data Points:**

*   **Final Level Reached:** The primary performance metric, indicating the highest speed/difficulty the user could manage.
*   **Score:** A composite score reflecting overall performance.
*   **Accuracy (Hits vs. Misses):** The ratio of correct key presses to total key presses.
*   **Reaction Times:** A log of the time taken for each correct key press.
*   **Average Reaction Time & Variability:** The mean and standard deviation of reaction times, indicating central tendency and consistency.
*   **Performance Over Time:** Analysis of accuracy and reaction time across the duration of the game to check for fatigue effects.
*   **Event Log:** A detailed record of every letter spawn, key press (correct or incorrect), and level change.
*   **Completion Status:** Whether the user completed the full game duration.

**2. Inferred Behavioral Traits:**

*   **Processing Speed:** How quickly the user can perceive, identify, and respond to a stimulus. Measured by average reaction time.
*   **Sustained Attention (Vigilance):** The ability to maintain focus and consistent performance over a prolonged period of continuous stimuli.
*   **Cognitive Flexibility:** The ability to adapt performance to changing demands. In this game, it's measured by the ability to keep up as the pace of letter-spawning accelerates.
*   **Motor Accuracy / Response Inhibition:** The ability to execute the correct motor response (key press) and inhibit incorrect ones, measured by the accuracy rate.
*   **Performance Under Pressure:** The final level reached indicates how well an individual maintains performance as the cognitive load and time pressure increase.

**3. Bi-Directional Dimensions:**

*   **Fast Processor <-> Slow Processor:** Directly measured by the average reaction time.
*   **Adaptable Under Pressure <-> Overwhelmed by Pressure:** Measured by the final level achieved. Higher levels indicate a greater ability to handle increasing task demands.
*   **Accurate <-> Error-Prone:** Measured by the overall accuracy percentage.
*   **High Cognitive Stamina <-> Easily Fatigued:** Inferred by comparing performance (accuracy, reaction time) between the first and second halves of the game. A significant drop-off suggests fatigue.
*   **Consistent Performer <-> Variable Performer:** Measured by the standard deviation of reaction times. Low variability indicates high consistency.

## Game 12: Spatial Working Memory Challenge (Memory Cards)

This game is a version of the classic card-matching (Concentration) game, designed to assess **spatial working memory**. The user must find pairs of matching cards on a grid that increases in size with each successfully completed level. The task requires holding the location and identity of previously seen cards in memory.

**1. Behavioral Data Points:**

*   **Highest Level Reached:** The primary metric, representing the user's maximum spatial working memory capacity for this task (i.e., the largest grid they could solve).
*   **Moves per Level:** The number of card flips made to complete a level. A lower number indicates greater efficiency.
*   **Accuracy:** The ratio of correct matches to total moves. High accuracy reflects an efficient search strategy and strong memory.
*   **Time per Level:** The duration taken to solve each grid.
*   **Event Log:** A detailed log of every card flip, including the card's position and icon, whether it was a match or mismatch, and the time of the event.
*   **Score:** A composite score calculated from the level reached, total moves, and total time, reflecting overall performance.
*   **Completion Status:** Whether the user progressed through all levels or quit mid-game.

**2. Inferred Behavioral Traits:**

*   **Spatial Working Memory Capacity:** The core trait measured. This is the ability to temporarily store and manipulate visual-spatial information, directly indicated by the highest level completed.
*   **Cognitive Strategy & Efficiency:** The effectiveness of the user's search pattern. An efficient player makes fewer redundant moves, indicating a systematic approach.
*   **Attention and Concentration:** The ability to focus on the task, encode card locations, and avoid careless errors.
*   **Visual Learning:** Inferred by observing whether the user's efficiency (moves per card) improves across levels, suggesting they are refining their strategy.

**3. Bi-Directional Dimensions:**

*   **High Capacity <-> Low Capacity (Working Memory):** Directly measured by the highest level the user can successfully complete.
*   **Efficient <-> Inefficient (Cognitive Strategy):** Measured by the number of moves and time taken relative to the minimum possible for a given level. Fewer moves and less time indicate higher efficiency.
*   **Systematic <-> Unsystematic (Search Pattern):** Inferred from the event log. A systematic player is less likely to re-flip a card whose match is already known or whose location has been clearly established.
*   **Focused <-> Distractible:** A high number of non-optimal moves (e.g., flipping a card that was just seen) or long pauses between flips could indicate distractibility or a lapse in attention.

## Game 13: The Trust Dilemma (Money Exchange 2)

This is a multi-round **Trust Game**, a canonical experiment in behavioral economics. The user decides how much of their money to invest with a partner. The invested amount is multiplied, and the partner (an AI with a specific personality) decides how much to return. The game measures trust, risk-taking, and the ability to model another's behavior.

**1. Behavioral Data Points:**

*   **Investment Amounts:** The amount of money the user sends to the partner in each of the 15 rounds.
*   **Partner's Return Amounts:** The amount of money the AI partner sends back in each round.
*   **Player's Balance Over Time:** The round-by-round fluctuation of the user's total money.
*   **Partner's Trust Level:** A dynamic metric within the game that reflects how the AI partner's trust in the player changes based on their investment history.
*   **Partner's AI Personality:** The underlying behavioral archetype of the AI partner for the game (e.g., 'Trustworthy', 'Erratic', 'Selfish').
*   **Event Log:** A detailed record of each round's transaction: amount sent, amount returned, resulting profit/loss, and the partner's trust level before and after the transaction.
*   **Final Balance:** The primary score, reflecting the user's overall success.

**2. Inferred Behavioral Traits:**

*   **Propensity to Trust:** The willingness to make oneself vulnerable to another's actions, measured by the initial and average investment amounts.
*   **Risk-Taking in Social Contexts:** The degree to which a user is willing to risk resources for a potential social and financial gain.
*   **Reciprocity and Fairness:** The user's tendency to reward positive actions (high returns) with continued or increased trust (high investments).
*   **Betrayal Aversion & Forgiveness:** The user's reaction following a 'betrayal' (a low return on a high investment). Do they immediately withdraw trust, or are they willing to give the partner another chance?
*   **Strategic Thinking & Mental Model Formation:** The ability to learn the partner's behavioral pattern (personality) and adapt one's investment strategy to maximize returns.

**3. Bi-Directional Dimensions:**

*   **Trusting <-> Distrustful:** Measured by the average percentage of their balance the user invests. High average investment indicates high trust.
*   **Strategic <-> Naive:** A strategic player's investments will correlate with the partner's behavior (e.g., investing more with a trustworthy partner, less with a selfish one). A naive player might invest randomly or use a fixed strategy regardless of feedback.
*   **Forgiving <-> Punishing:** A forgiving player will resume investing after a betrayal, while a punishing player will significantly reduce or stop investments for one or more rounds.
*   **Adaptive <-> Rigid:** An adaptive player changes their investment strategy based on the partner's personality, while a rigid player uses the same approach regardless of who they are interacting with.

## Game 14: Inductive Reasoning Challenge (Pattern Completion)

This game is a classic test of **fluid intelligence**, a core component of general intelligence. It requires the user to identify the underlying logical rule in a series of numbers and then select the number that correctly completes the sequence. The patterns range from simple arithmetic progressions to more complex alternating or power series.

**1. Behavioral Data Points:**

*   **Score & Final Difficulty:** The primary metrics of performance. The score reflects overall success, and the final difficulty level indicates the complexity of the problems the user was able to solve.
*   **Accuracy:** The percentage of correctly solved patterns.
*   **Reaction Time:** The time taken to solve each problem.
*   **Pattern Type Analysis:** A breakdown of performance (accuracy, reaction time) for each category of pattern (e.g., Arithmetic, Geometric, Alternating Series).
*   **Event Log:** A detailed record of each round, including the pattern presented, the options, the user's choice, its correctness, and the reaction time.
*   **Completion Status:** Whether the user completed all rounds.

**2. Inferred Behavioral Traits:**

*   **Fluid Intelligence / Inductive Reasoning:** The core trait being measured. This is the ability to reason, solve novel problems, and identify patterns independent of acquired knowledge.
*   **Abstract Reasoning:** The capacity to understand and work with abstract concepts and logical relationships.
*   **Cognitive Flexibility:** The ability to shift between different mental sets or problem-solving strategies, which is necessary to identify the different types of patterns presented.
*   **Working Memory:** The user must hold the sequence in their working memory while they test different hypotheses about the underlying rule.

**3. Bi-Directional Dimensions:**

*   **High <-> Low Fluid Intelligence:** Directly measured by the score and the difficulty level of the problems solved. Higher scores on more complex patterns indicate higher fluid intelligence.
*   **Systematic <-> Heuristic Problem-Solver:** A systematic thinker may have longer reaction times but higher accuracy, especially on difficult problems. A heuristic or intuitive thinker might be faster but more prone to errors. This is inferred by analyzing the relationship between speed and accuracy.
*   **Cognitively Flexible <-> Cognitively Rigid:** A flexible thinker will perform well across various pattern types. A rigid thinker might master one type (e.g., arithmetic) but struggle when the underlying logic changes (e.g., to a power series). This is analyzed by comparing performance across pattern categories.
*   **Quick Thinker <-> Deliberate Thinker:** Measured by the average reaction time for correctly solved problems. This reflects the speed at which an individual can process information and arrive at a logical conclusion.

## Game 15: Temporal Reflex Challenge (Reaction Timer)

This game provides a direct measure of **simple reaction time**, one of the most basic and fundamental cognitive processes. The user must respond as quickly as possible to a visual stimulus, but only after it appears. Responding too early is penalized.

**1. Behavioral Data Points:**

*   **Average Reaction Time (ms):** The mean time taken to respond to the stimulus across all valid trials. This is the primary measure of processing speed.
*   **Reaction Time Variability:** The standard deviation of reaction times. This indicates the consistency of the user's performance.
*   **Early Clicks:** The number of times the user responded *before* the stimulus appeared. This is a measure of impulsivity or poor response inhibition.
*   **Score:** A composite score calculated from the average reaction time and penalized for early clicks.
*   **Event Log:** A detailed log of each trial, including the random delay before the stimulus, the user's reaction time, and whether the response was valid or premature.
*   **Completion Status:** Whether the user completed all trials or quit early.

**2. Inferred Behavioral Traits:**

*   **Processing Speed:** The speed at which the brain can perceive a stimulus and execute a motor response. This is directly measured by the average reaction time.
*   **Response Inhibition:** The ability to withhold a prepotent or automatic response. This is inferred from the number of early clicks.
*   **Vigilance / Sustained Attention:** The ability to maintain focus while waiting for an unpredictable stimulus. High variability in reaction time can suggest lapses in attention.
*   **Performance Consistency:** The ability to perform at a stable level over time, measured by the standard deviation of reaction times.

**3. Bi-Directional Dimensions:**

*   **Fast <-> Slow Processor:** Directly measured by the average reaction time. A lower average time indicates a faster processor.
*   **Impulsive <-> Controlled:** A high number of early clicks suggests an impulsive response style, whereas a low number indicates good response control.
*   **Consistent <-> Inconsistent:** A low standard deviation in reaction times indicates a consistent performer. A high standard deviation suggests performance that fluctuates, possibly due to lapses in attention or fatigue.
*   **Vigilant <-> Inattentive:** While not directly measured, chronic inconsistency and a high number of outliers in reaction time could suggest a more inattentive state.

## Game 16: Cognitive Sorting Challenge

This game is an adaptive test of **executive functioning**, specifically focused on categorization speed and accuracy under increasing time pressure. Users must sort icons into their correct categories (e.g., Fruit, Animal, Vehicle) as quickly as possible. The time allowed for each decision shrinks with every correct answer.

**1. Behavioral Data Points:**

*   **Score:** A composite metric reflecting both speed and accuracy.
*   **Accuracy:** The percentage of correctly categorized items.
*   **Average Reaction Time (RT):** The average time taken for correct categorizations.
*   **Final Time Limit:** The shortest time limit the user was able to perform under, indicating their peak processing speed for this task.
*   **Error Analysis:** A breakdown of errors into incorrect categorizations (pressing the wrong key) and missed trials (running out of time).
*   **Event Log:** A detailed record of each trial, including the stimulus, the user's response, reaction time, correctness, and the time limit for that trial.
*   **Completion Status:** Whether the user completed all trials.

**2. Inferred Behavioral Traits:**

*   **Categorization Speed:** The ability to rapidly and accurately classify information based on learned rules.
*   **Executive Functioning:** The higher-order cognitive processes that control and coordinate other cognitive abilities, including mental flexibility, planning, and inhibition.
*   **Processing Speed Under Pressure:** How well an individual can maintain performance as cognitive load and time constraints increase.
*   **Attention and Focus:** The ability to sustain concentration on a repetitive, fast-paced task.

**3. Bi-Directional Dimensions:**

*   **Fast <-> Slow Categorizer:** Measured by the average reaction time and the final time limit achieved. A lower RT and a shorter final time limit indicate a faster categorizer.
*   **Accurate <-> Inaccurate Sorter:** Directly measured by the overall accuracy rate. A high accuracy rate suggests strong and reliable category knowledge.
*   **Resilient <-> Brittle Under Pressure:** A resilient individual will maintain high accuracy even as the time limit decreases. A brittle performer's accuracy will degrade significantly as the pressure mounts. This is seen by comparing accuracy in the first half of the game versus the second half.
*   **Decisive <-> Hesitant:** A decisive player will have consistently fast reaction times. A hesitant player may have a higher average reaction time and greater variability, with more missed trials due to timeouts.

## Game 17: Inhibitory Control Challenge (Stop-Signal Task)

This is a classic Stop-Signal Task, a premier tool for measuring **response inhibition**, a critical executive function. The user is conditioned to make a rapid response (e.g., press an arrow key) but must cancel or inhibit that action on a fraction of trials when a "stop signal" is presented.

**1. Behavioral Data Points:**

*   **Stop-Signal Reaction Time (SSRT):** The core metric. It is the estimated time it takes for the brain to successfully cancel a motor command that is already underway. A lower SSRT indicates more efficient inhibitory control.
*   **Go-Trial Reaction Time (Go RT):** The average reaction time on trials that did not feature a stop signal. This provides a baseline for the user's processing speed.
*   **Stop-Trial Accuracy:** The percentage of trials where the user successfully withheld their response when a stop signal was presented.
*   **Go-Trial Accuracy:** The percentage of correct responses on go trials.
*   **Stop-Signal Delay (SSD):** The time delay between the initial "go" stimulus and the "stop" signal. This delay is adaptively adjusted based on performance to target a ~50% success rate on stop trials.
*   **Event Log:** A detailed trial-by-trial log including trial type (go/stop), stimulus, response, RT, and the SSD for that trial.

**2. Inferred Behavioral Traits:**

*   **Response Inhibition:** The primary trait measured. The ability to override a prepotent, or automatic, response.
*   **Impulsivity:** Poor performance on this task (a long SSRT) is often linked to higher levels of impulsivity.
*   **Attention & Vigilance:** The user must remain attentive to respond quickly on go trials while also being vigilant for the less frequent stop signals.
*   **Strategic Pacing:** Some users may intentionally slow down their Go RTs to make it easier to succeed on stop trials. This trade-off between speed and control is itself a valuable behavioral marker.

**3. Bi-Directional Dimensions:**

*   **High <-> Low Inhibitory Control:** A low SSRT indicates high control (less impulsive), while a high SSRT indicates low control (more impulsive).
*   **Proactive <-> Reactive Control:** A user exhibiting proactive control might slow down all their responses (high Go RT) to better prepare for a potential stop signal. A reactive user will have fast Go RTs and rely solely on their ability to cancel the action after the stop signal appears.
*   **Consistent <-> Inconsistent Performer:** High variability in Go RTs or in stop-trial success can indicate fluctuating attention or an unstable inhibitory process.
*   **Fast <-> Slow Processor:** The Go RT provides a clean measure of simple choice reaction time, which can be compared to other reaction time measures from different games.

## Game 18: Cognitive Control Challenge (Stroop Test)

This is the classic Stroop Test, a gold-standard measure of **selective attention** and **cognitive inhibition**. The user is presented with a word (a color name) printed in a specific color of ink. The task is to identify the ink color while ignoring the word itself, which becomes difficult when the two are incongruent (e.g., the word "Blue" printed in red ink).

**1. Behavioral Data Points:**

*   **Stroop Interference Effect:** The primary metric, calculated as `(Average Incongruent RT) - (Average Congruent RT)`. A larger value indicates greater interference and more difficulty exercising cognitive control.
*   **Congruent vs. Incongruent Reaction Times (RTs):** The average RT for trials where the word and ink color match (congruent) versus when they conflict (incongruent). The congruent RT serves as a baseline processing speed.
*   **Accuracy (Overall, Congruent, Incongruent):** Accuracy percentages are calculated for all trial types. A significant drop in accuracy on incongruent trials is a strong indicator of interference.
*   **Adaptive Time Limit:** The game adjusts the response time limit based on performance. The final time limit reflects the pace the user could successfully maintain.
*   **Error Analysis:** Examining the nature of errors. Errors on incongruent trials often involve incorrectly choosing the color named by the word, demonstrating a failure of inhibition.
*   **Event Log:** A detailed trial-by-trial record, including the stimulus word, ink color, trial type, user's response, correctness, and RT.

**2. Inferred Behavioral Traits:**

*   **Selective Attention:** The capacity to focus on the relevant stimulus feature (ink color) and filter out the irrelevant, distracting feature (the word).
*   **Cognitive Inhibition:** The core executive function measured. The ability to suppress a prepotent, automatic, and dominant response (reading the word) in favor of a less automatic one (naming the color).
*   **Processing Speed:** The congruent RT provides a baseline measure of how quickly the user can make a simple choice response when there is no cognitive conflict.
*   **Cognitive Flexibility:** The ability to switch between processing the word's meaning and its visual properties, although this is a secondary trait in this task.

**3. Bi-Directional Dimensions:**

*   **High <-> Low Cognitive Inhibition:** A small Stroop effect indicates high inhibition (good at ignoring the word), while a large effect indicates low inhibition (easily distracted by the word).
*   **Automatic <-> Controlled Processor:** Individuals who are more susceptible to the Stroop effect rely more on automatic processing (reading). Those who can overcome it exhibit stronger controlled, goal-directed processing.
*   **Focused <-> Distractible:** Low error rates and a small Stroop effect are characteristic of a focused individual. High error rates and a large effect suggest higher distractibility.
*   **Fast <-> Slow Processing Speed:** The baseline speed of response, as measured by the congruent reaction time, independent of the inhibition task.

## Game 19: Progressive Planning Challenge (Tower of Hanoi)

This is a digital version of the classic Tower of Hanoi puzzle, a quintessential test of **planning, foresight, and problem-solving abilities**. The user must move a stack of progressively smaller disks from a starting peg to a target peg, adhering to simple rules. The challenge scales in difficulty, providing insight into the limits of a user's executive functions.

**1. Behavioral Data Points:**

*   **Final Level Reached:** The highest number of disks the user successfully managed to solve. This is a primary indicator of their planning capacity.
*   **Solution Efficiency (Moves vs. Optimal):** The ratio or difference between the user's total moves and the mathematically optimal number of moves (`2^n - 1`, where `n` is the number of disks). This is a direct measure of problem-solving efficiency.
*   **Time per Level:** The time taken to solve the puzzle at each level of difficulty. A sharp increase in time can indicate the user is approaching their cognitive limit.
*   **Thinking Time (Time per Move):** The average time between moves. Long pauses may indicate planning, while rapid, inefficient moves suggest a trial-and-error approach.
*   **Error Rate:** The number of invalid moves attempted (e.g., placing a larger disk on a smaller one).
*   **Event Log:** A rich, move-by-move log capturing the entire solution path, including pauses, errors, and the sequence of moves for each level.

**2. Inferred Behavioral Traits:**

*   **Planning & Foresight:** The core trait measured. The ability to mentally simulate future steps and formulate a multi-step plan to reach a goal.
*   **Problem-Solving Strategy:** The ability to break down a complex problem into smaller, manageable sub-goals. Efficient solvers apply a consistent, recursive strategy.
*   **Working Memory:** The user must hold the state of the puzzle, the rules, and their current plan in mind. Performance is heavily constrained by working memory capacity.
*   **Persistence & Frustration Tolerance:** The willingness to stick with a challenging problem. Analyzing whether a user abandons the game when the difficulty spikes is revealing.

**3. Bi-Directional Dimensions:**

*   **Strategic Planner <-> Trial-and-Error Solver:** A strategic planner will produce a solution with a near-optimal number of moves. A trial-and-error solver will have a much higher move count, more errors, and less predictable move patterns.
*   **Efficient <-> Inefficient Problem-Solver:** This is measured directly by the moves-to-optimal ratio and the time taken. An efficient solver finds the shortest path quickly.
*   **High <-> Low Working Memory Capacity:** An individual with high working memory capacity will be able to solve puzzles with more disks and will likely do so more efficiently.
*   **Methodical <-> Impulsive:** A methodical player will have longer, more consistent thinking times between moves. An impulsive player will make moves quickly, often leading to more errors and inefficient solutions.

## Game 20: Adaptive Risk Challenge (Balloon Analogue Risk Task)

This is a version of the Balloon Analogue Risk Task (BART), a standardized assessment of **risk-taking propensity** and **decision-making under uncertainty**. The user repeatedly pumps a virtual balloon, earning a small amount of money with each pump. They can 'cash out' at any point to bank the earnings for that round, but if they pump too many times, the balloon will burst, and they lose all potential earnings for that round.

**1. Behavioral Data Points:**

*   **Adjusted Average Pumps:** The average number of pumps on balloons that were successfully cashed out (i.e., did not burst). This is the primary measure of risk-taking. A higher number indicates greater risk-taking.
*   **Total Number of Bursts:** The total count of rounds where the balloon popped. This reflects the negative consequences of the user's risk-taking strategy.
*   **Total Winnings:** The final score, which reflects the overall effectiveness of the user's risk-taking strategy.
*   **Behavioral Adaptation:** Analyzing the number of pumps on the trial immediately following a burst vs. following a successful cash-out. A significant decrease in pumps after a burst indicates learning and adaptation.
*   **Pump Latency:** The time taken between pumps. Faster pumping can indicate higher impulsivity.
*   **Event Log:** A detailed round-by-round log including the number of pumps, cash-out decisions, burst events, and the state of winnings.

**2. Inferred Behavioral Traits:**

*   **Risk-Taking Propensity:** The core trait measured. The degree to which an individual is willing to engage in a behavior that has the potential for reward but also carries a risk of loss.
*   **Decision Making Under Uncertainty:** The task requires making choices where the outcome is probabilistic, not certain.
*   **Impulsivity vs. Self-Control:** The decision to keep pumping can be seen as an impulsive choice for immediate gratification (a higher potential reward), while cashing out represents self-control.
*   **Feedback Responsiveness:** How a user's behavior changes in response to negative feedback (a burst) or positive feedback (a successful cash-out).

**3. Bi-Directional Dimensions:**

*   **Risk-Seeking <-> Risk-Averse:** A risk-seeking individual will have a high adjusted average pump count and likely more bursts. A risk-averse person will cash out early with fewer pumps.
*   **Impulsive <-> Deliberate:** An impulsive player may pump quickly and escalate their risk-taking without regard to consequences. A deliberate player may have longer latencies and a more stable pumping strategy.
*   **Adaptive <-> Rigid Strategist:** An adaptive player will significantly reduce their pumping after a burst. A rigid strategist will maintain a similar number of pumps regardless of the previous outcome.
*   **Reward-Sensitive <-> Loss-Averse:** A reward-sensitive player is driven by the potential for a big win, leading to more pumps. A loss-averse player is more motivated by the fear of the balloon bursting, leading to more cautious play.

## Game 21: Working Memory Challenge (Digit Span)

This is a classic Digit Span task, a cornerstone of cognitive assessment used to measure **short-term and working memory capacity**. The game presents two distinct phases: a forward span, where the user recalls a sequence of numbers in order, and a backward span, where they must recall the sequence in reverse.

**1. Behavioral Data Points:**

*   **Maximum Forward Span:** The longest sequence of digits the user could correctly recall in the order they were presented. This is a direct measure of short-term memory capacity.
*   **Maximum Backward Span:** The longest sequence of digits the user could correctly recall in reverse order. This is a key measure of working memory, as it requires both storage and mental manipulation.
*   **Span Difference:** The difference between the forward and backward spans (`Forward Span - Backward Span`). A larger difference can indicate a specific difficulty with manipulating information versus simply storing it.
*   **Trial-by-Trial Accuracy:** The log of correct and incorrect responses at each span length for both tasks. This shows how performance changes as cognitive load increases.
*   **Response Time:** The time taken to input the sequence after it has been presented.
*   **Event Log:** A detailed record of each trial, including the task type (forward/backward), the presented sequence, the user's input, and the outcome.

**2. Inferred Behavioral Traits:**

*   **Short-Term Memory Capacity:** The ability to hold a small amount of information in an active, easily accessible state for a brief period. Directly measured by the forward span.
*   **Working Memory:** A more complex executive function involving the ability to store, maintain, and manipulate information. Directly measured by the backward span.
*   **Attention and Concentration:** Successful performance requires sustained focus during the presentation of the digits to ensure they are encoded correctly.
*   **Cognitive Processing Speed:** While not the primary measure, the speed at which a user can recall and input the sequence can be an indicator of processing efficiency.

**3. Bi-Directional Dimensions:**

*   **High <-> Low Short-Term Memory Capacity:** A direct comparison based on the maximum forward span. Most adults typically score between 5 and 9 items.
*   **High <-> Low Working Memory Capacity:** A direct comparison based on the maximum backward span. This is generally about one or two items fewer than the forward span.
*   **Efficient <-> Inefficient Mental Manipulation:** An individual with a small difference between their forward and backward span is relatively efficient at manipulating information. A large gap suggests a specific cost or difficulty in this area.
*   **Attentive <-> Inattentive:** An inconsistent performance, such as failing at a short span length after succeeding at a longer one, may indicate lapses in attention rather than a true memory capacity limit.

## Game 22: Economic Fairness Challenge (Ultimatum Game)

This is an implementation of the **Ultimatum Game**, a canonical experiment from behavioral economics designed to measure social preferences, including **altruism**, **fairness norms**, and **costly punishment**. The user plays in two roles: as a Proposer who offers a split of $10, and as a Responder who can accept or reject that split. If rejected, neither party gets anything.

**1. Behavioral Data Points:**

*   **Average Offer Made (as Proposer):** The average amount of money the user offers to their partner when they are the Proposer. This is a primary measure of altruism and strategic fairness.
*   **Minimum Acceptance Threshold (as Responder):** The lowest offer the user is willing to accept from a partner. Rejecting low, but non-zero, offers is a measure of costly punishment.
*   **Rejection Rate:** The percentage of offers the user rejects as the Responder. A high rejection rate for low offers indicates a strong preference for fairness.
*   **Behavioral Adaptation to Partner Profile:** The game includes partners with different fairness profiles (e.g., fair, selfish, generous). The data shows how the user changes their own offers and rejection thresholds in response to these different social contexts.
*   **Total Winnings:** The final score, reflecting the overall success of the user's social and economic strategy.
*   **Event Log:** A detailed round-by-round log of the user's role, the partner's profile, the offer made or received, and the accept/reject decision.

**2. Inferred Behavioral Traits:**

*   **Sense of Fairness:** The degree to which an individual values equitable outcomes over pure self-interest. This is seen in both generous offers and the rejection of unfair ones.
*   **Altruism:** The willingness to benefit others at a cost to oneself. Proposers offering a 50/50 split are demonstrating altruistic or fair behavior.
*   **Strategic Social Cognition:** The ability to model the intentions and likely actions of others and adapt one's strategy accordingly. This is observed when users adjust their behavior based on the partner's profile.
*   **Negative Reciprocity (Costly Punishment):** The willingness to incur a personal cost (losing a small gain) to punish someone for unfair or anti-social behavior (making a low offer).

**3. Bi-Directional Dimensions:**

*   **Altruistic <-> Self-Interested:** An altruistic player will make generous offers (e.g., $4-$5). A purely self-interested player will make the lowest possible offers (e.g., $1).
*   **Fairness-Oriented <-> Profit-Maximizing:** A fairness-oriented player will reject low offers as a Responder, enforcing a social norm. A profit-maximizing player will accept any non-zero offer, as any gain is better than none.
*   **Strategically Adaptive <-> Unconditionally Consistent:** An adaptive player will offer more to a fair partner and less to a selfish one. A consistent player might offer $5 in all situations, regardless of context.
*   **Punitive <-> Forgiving:** A punitive individual will have a high rejection threshold, punishing any perceived slight. A forgiving or rational player will have a low threshold, overlooking unfairness for a small gain.

## Game 23: Facial Emotion Perception

This task is a standardized assessment of **emotion recognition**, a core component of **social cognition** and **emotional intelligence**. The user is shown a series of faces expressing one of six basic emotions (happy, sad, angry, fear, surprise, disgust) and must correctly identify the emotion.

**1. Behavioral Data Points:**

*   **Overall Accuracy:** The percentage of emotions correctly identified across all trials. This is the primary measure of emotion recognition ability.
*   **Reaction Time:** The average time taken to make a decision. This can indicate the automaticity and efficiency of social processing.
*   **Confusion Matrix:** A breakdown of errors, showing which emotions are most often confused with each other (e.g., consistently mislabeling 'fear' as 'surprise').
*   **Emotion-Specific Accuracy:** The accuracy calculated for each of the six emotions individually. This can reveal specific strengths or deficits in recognizing particular emotions.
*   **Event Log:** A trial-by-trial record of the presented emotion, the user's choice, whether it was correct, and the reaction time.

**2. Inferred Behavioral Traits:**

*   **Social Cognition:** The ability to process and interpret social information. High accuracy indicates well-developed social-perceptual skills.
*   **Empathy (Cognitive Component):** The capacity to understand another person's emotional state. Accurate emotion recognition is a prerequisite for cognitive empathy.
*   **Attention to Social Cues:** The task requires focusing on subtle configurations of facial muscles to make a correct judgment.
*   **Potential for Perceptual Biases:** A pattern of specific errors (e.g., a bias towards interpreting neutral or ambiguous faces as angry) can be revealed by the confusion matrix.

**3. Bi-Directional Dimensions:**
*   **High <-> Low Emotion Recognition Skill:** A direct measure based on overall accuracy. Individuals with high accuracy are adept at reading social cues.
*   **Efficient <-> Inefficient Social Processor:** This is inferred from reaction times. Faster, accurate responses suggest more automatic and efficient processing of social signals.
*   **Specific Emotional Sensitivity <-> Insensitivity:** An analysis of emotion-specific accuracy can show if a person is highly attuned to certain emotions (e.g., threat-related emotions like anger and fear) while being less sensitive to others.
*   **Positive <-> Negative Emotion Bias:** Comparing accuracy for positive emotions (happy) versus negative emotions (angry, sad, fear, disgust) can indicate a potential bias in social perception.


## Game 25: Flanker Task

This is a version of the Flanker Task, a widely used measure of **executive control** and **selective attention**. The user is presented with a row of arrows and must identify the direction of the central arrow while ignoring the flanking arrows.

**1. Behavioral Data Points:**

*   **Reaction Time (RT):** The time elapsed between the appearance of the stimulus (arrows) and the user's keypress. This is recorded for each trial.
*   **Accuracy:** Whether the user's response was correct or incorrect for each trial. A response is correct if the key pressed corresponds to the direction of the central arrow.
*   **Trial Type:** The condition of each trial is recorded. The conditions are:
    *   **Congruent:** The flanking arrows point in the same direction as the central arrow (e.g., `>>>>>`).
    *   **Incongruent:** The flanking arrows point in the opposite direction to the central arrow (e.g., `>><>>`).
    *   **Neutral:** The stimulus consists of non-arrow characters (e.g., `++>++`).
*   **Flanker Effect:** This is a calculated metric, representing the difference in reaction time between incongruent and congruent trials (`Incongruent RT - Congruent RT`).
*   **Timeouts:** The game records if the user failed to respond within the allocated time for a trial.
*   **Game Events:** The system logs various events with timestamps:
    *   `game_start`: Marks the beginning of the game.
    *   `trial_start`: Marks the beginning of each trial.
    *   `response`: Records the user's keypress, whether it was correct, and the reaction time.
    *   `game_end`: Marks the natural completion of the game.
    *   `game_abandoned`: Logs if the user exits the game before completion.
*   **Completion Status:** The game tracks whether it was 'completed' or 'abandoned'.

**2. Inferred Behavioral Traits:**

*   **Attention Control & Selective Attention:** The core of the Flanker Task is to measure how well an individual can focus on a target stimulus while ignoring distracting information. A high Flanker effect (much slower RTs on incongruent trials) suggests difficulty in filtering out distractions.
*   **Cognitive Flexibility:** The ability to switch between different rules or tasks. While not the primary measure, the mix of trial types requires the user to consistently apply the "focus on the center" rule, testing their cognitive stability.
*   **Processing Speed:** The average reaction time on correct trials, particularly in neutral or congruent conditions, provides a baseline for how quickly the user can process visual information and execute a motor response.
*   **Impulsivity vs. Self-Control:** Fast, incorrect responses, especially on incongruent trials, can indicate impulsivity (responding before fully processing the stimulus). Conversely, consistently accurate but slower responses may suggest a more cautious or controlled approach.
*   **Resilience to Distraction:** A lower Flanker effect indicates greater resilience to misleading information. This is a measure of how effectively one's cognitive control system can override automatic responses.
*   **Task Engagement & Persistence:** The completion status ('completed' vs. 'abandoned') directly measures the user's willingness to see a task through to the end. Analyzing the number of trials completed before abandoning the game can also provide insights into their frustration tolerance.
*   **Learning/Adaptation:** While not explicitly measured as a single metric, analyzing reaction times and accuracy over the course of the 96 trials could reveal learning effects, such as a decrease in the Flanker effect as the user becomes more accustomed to the task.

**3. Bi-Directional Dimensions:**

*   **Focused <-> Distractible:** This dimension is directly measured by the Flanker effect. A low score indicates a focused individual, while a high score suggests someone who is more easily distracted.
*   **Impulsive <-> Deliberate:** This can be inferred from the speed-accuracy trade-off. Quick, error-prone responses point towards impulsivity, whereas slow, accurate responses suggest a more deliberate and cautious style.
*   **Cognitively Flexible <-> Rigid:** While this game is not the strongest measure for this trait, consistent performance across different trial types suggests flexibility, whereas a significant drop in performance on incongruent trials could hint at cognitive rigidity when faced with conflicting information.
*   **Persistent <-> Gives Up Easily:** This is directly measured by the completion status of the game. Completing the game indicates persistence, while abandoning it suggests a lower threshold for frustration or a tendency to give up.
*   **Quick Thinker <-> Methodical:** This is reflected in the overall average reaction time. A faster RT suggests quick thinking, while a slower RT could indicate a more methodical and careful approach to problem-solving.

