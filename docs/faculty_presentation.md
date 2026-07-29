# SHADE-IDS - Faculty Presentation Script and Q&A Prep

A full walkthrough script for explaining the project to faculty, plus likely
questions with prepared answers.

---

## Presentation Script

### Introduction

Good [morning/afternoon] sir/ma'am. My project is called SHADE-IDS - an Explainable
Hybrid Intrusion Detection System. In simple terms, it's a smart security system for
computer networks that doesn't just say 'this is an attack,' it also tells you why it
thinks so. I built this over four weeks, covering data handling, machine learning, an
anomaly detector, explainability, and finally a working application with a dashboard,
along with a full research paper and a patent disclosure.

### The Problem I'm Solving

Right now, network security tools have two big weaknesses. The first kind, called
signature-based systems, work like a list of 'known criminals' - they only catch
attacks that match a pattern someone has already written a rule for. So if a completely
new kind of attack shows up, a zero-day attack, these systems are blind to it. The
second kind, machine learning-based systems, are smarter and can catch a wider range of
attacks, but they behave like a black box. They just say 'attack' or 'not attack' with
no explanation, so a security analyst has no way to quickly verify if the alert is real
or trust why it happened. My project tries to fix both these problems at once.

### What I Actually Built - The Architecture

I built a hybrid system with three detection layers working together:

The first layer is a signature rule layer. These are simple, fast, human-readable
rules - for example, if there are very few packets but they're trying many different
ports, that's a port scan; if there's a huge number of connection attempts to a login
service like FTP, that's a brute-force attempt. This layer is instant and doesn't need
any machine learning.

The second layer is supervised machine learning. I trained two models, Random Forest
and XGBoost, on a real, standard network traffic dataset called UNSW-NB15, which has
about 257,000 network flows, both normal and attack traffic across nine different
attack categories. These models learned to classify traffic as attack or benign, and
they achieved around 95% accuracy and a ROC-AUC of 0.99, which is a very strong result.

The third layer is the most interesting one, a benign-only autoencoder. This is a
neural network that I trained only on normal traffic, it never sees a single attack
example during training. It learns what 'normal' looks like, and when new traffic comes
in, it tries to reconstruct it. If the traffic is normal, it reconstructs it well, with
low error. But if it's an attack, even a completely new type it's never seen, it
reconstructs it poorly, and that high reconstruction error is the signal that something
is wrong. This is how the system can catch zero-day attacks without ever needing
labeled attack data for training.

Finally, on top of all three layers, I added an explainability layer using something
called SHAP, which stands for SHapley Additive exPlanations. For every single alert,
SHAP tells us exactly which features of that network flow, for example the
time-to-live value, the number of bytes sent, or the connection state, pushed the model
toward calling it an attack. So instead of just a red alert, the analyst sees a clear
breakdown of why.

### Tech Stack

For the core machine learning, I used Python with scikit-learn for Random Forest,
XGBoost library for the gradient boosting model, and PyTorch to build and train the
autoencoder neural network. For explainability I used the SHAP library. For data
handling I used pandas and numpy. The whole application front end, the dashboard, is
built with Streamlit, which lets me turn Python code directly into an interactive web
app, so it runs in any browser without needing to install anything separate. For
version control and weekly submissions I used Git and GitHub, and I also set up
automated testing using GitHub Actions, so every time I push code, a small test suite
runs automatically to make sure nothing is broken.

### Real Research Behind It

This wasn't just an application, I also ran a proper research study. I used a method
called leave-one-family-out, where I hold out an entire attack category completely,
the model never sees it during training, and then test whether the system can still
detect it. This simulates a true zero-day scenario. I did this across all nine attack
categories in UNSW-NB15, and then repeated the entire study on a second, completely
independent dataset called CIC-IDS2017, to make sure my findings weren't just a
coincidence of one dataset. The result was consistent across both: supervised models
generalize surprisingly well to unseen attacks in most cases, but there are always one
or two blind spots, like the Fuzzers category in UNSW-NB15, or Bots and Port Scanning
in CIC-IDS2017, where even the anomaly detector struggles. I used SHAP to explain why,
and even ran an ablation test, removing the most important feature to see if the model
still worked, which showed some really interesting insights about feature redundancy.
This is written up as a full IEEE-format research paper, and I've also drafted a
patent disclosure for the hybrid explainable detection method.

### Live Demo - What I'll Show You Right Now

Walk through the dashboard at `http://localhost:8501`:

1. **Overview tab** - dataset and system structure.
2. **Detection Results tab** - RF and XGBoost both hit about 95% accuracy with a
   ROC-AUC of 0.9925 on known attacks. The autoencoder alone, with zero attack labels,
   still catches about 35% of attacks while only raising false alarms on 0.8% of normal
   traffic.
3. **Explainability tab** - the SHAP charts. One shows globally which features the
   model relies on most; the other shows a single alert broken down feature by
   feature.
4. **Live Signature Check tab** (interactive):
   - Set service to 'ftp', rate to something high like 5000, state to 'CON' - the
     system instantly flags it as a Brute Force attempt in real time.
   - Change back to normal values (service 'http', low rate, state 'FIN') - it says no
     signature matched, this would pass through as normal traffic.
   - This shows the system reacting live, not just showing pre-computed results.

### Future Scope

Multi-class detection with a proper 'unknown' category instead of a forced binary
decision. Validating on live, real-time network traffic instead of a static benchmark
dataset. Exploring adversarial robustness, testing whether an attacker could craft
traffic to fool the model, and building defenses against that. Moving from a local
dashboard to a fully cloud-hosted version, integrated into a real Security Operations
Center workflow.

### Conclusion

This project combines three complementary detection techniques, backed by real
experiments on two independent datasets, wrapped in a working explainable dashboard,
documented in a full research paper, and protected through a patent disclosure. It's a
complete pipeline from raw network data all the way to an explained, actionable
security alert.

---

## Q&A Prep

**Q1: Why not just use deep learning for everything instead of this hybrid approach?**

A pure deep learning model would still be a black box, and it would still need labeled
attack data to learn new attack types, so it would not solve the zero-day problem by
itself. My hybrid design uses supervised models for what they are good at, known
attacks, and a benign-only autoencoder for what supervised models cannot do, catching
attacks with no labels at all. Combining them, with signature rules as a fast first
pass, gives broader coverage than any single approach, and SHAP on top gives the
explainability that a plain deep learning model would not have.

**Q2: How is this different from existing commercial IDS tools like Snort or Suricata?**

Tools like Snort and Suricata are signature-based, so they only catch attacks with a
known rule. My system adds two more layers on top of that idea: supervised machine
learning for broader known-attack coverage, and a benign-only autoencoder specifically
for zero-day attacks that have no signature and no label at all. On top of that, every
alert comes with a SHAP explanation, which traditional signature tools do not provide.

**Q3: What datasets did you use and why these specifically?**

I used UNSW-NB15 and CIC-IDS2017, both are standard, widely cited benchmark datasets in
network intrusion detection research, so results are comparable to prior published
work. UNSW-NB15 has about 257,000 flows across nine attack categories. I used
CIC-IDS2017 as a second, independent dataset to check that my findings were not just a
coincidence of one dataset, and the same pattern held on both.

**Q4: Your autoencoder only catches 35% of attacks. Isn't that a weak result?**

That 35% is achieved with a very strict false-alarm budget of just 0.8%, and, more
importantly, with zero attack labels used in training. In a real deployment you would
not throw away the supervised models, you would use the autoencoder as a backup layer
specifically for the attack types the supervised models miss. My leave-one-family-out
experiments show that supervised models already generalize very well to most unseen
attacks, so the autoencoder's job is to cover the specific blind spots, not to replace
the supervised layer.

**Q5: What is SHAP and why did you choose it over other explainability methods?**

SHAP, SHapley Additive exPlanations, is based on a concept from game theory that fairly
distributes credit for a prediction among the input features. I chose it because it
gives both a global view, which features matter most overall, and a local, per-alert
view, why this specific flow was flagged, and it is one of the most widely used and
trusted explainability methods in machine learning research today.

**Q6: What is a leave-one-family-out experiment and why does it matter?**

Normally, machine learning models are tested by randomly splitting data into train and
test sets, but if an attack type appears in both the training and test data, the model
is not really being tested on anything new. In my leave-one-family-out method, I remove
an entire attack category completely from training and only show it to the model during
testing. This properly simulates a true zero-day scenario and gives a much more honest
measure of how well the model would perform against a genuinely new attack.

**Q7: What is the practical, real-world use case for this system?**

It's meant for a network operations center or a security team monitoring enterprise or
IoT traffic. Instead of just receiving a flood of unexplained alerts, an analyst sees
each alert with the exact features that caused it, which lets them verify and respond
much faster. The autoencoder layer also gives an organization some protection against
brand-new attacks even before a proper signature or labeled example exists for it.

**Q8: What were the biggest challenges you faced building this?**

Getting a fair comparison between the supervised models and the autoencoder was
tricky, since they produce very different kinds of scores, so I had to design an
evaluation protocol that compares them at a matched false-positive rate rather than
just comparing raw accuracy numbers. Another challenge was making sure the SHAP
explanations were computed efficiently, since some explainability methods are quite
slow on large datasets.

**Q9: Is this patentable? What exactly is the novel part?**

The novelty is in the specific combination, not any single piece in isolation. Signature
rules, supervised classifiers, and autoencoders all exist separately in prior work, but
combining all three into one pipeline, using the benign-only autoencoder specifically
to cover zero-day gaps left by the supervised models, and attaching a per-alert SHAP
explanation to every detection, is the inventive step described in the patent
disclosure.

**Q10: What would you do differently, or what is the biggest limitation right now?**

The biggest limitation is that both datasets are benchmark captures, not live
enterprise traffic, so absolute numbers might shift in a real deployment. I also use a
binary attack-versus-benign framing right now, so a proper multi-class 'unknown'
category, which I mentioned in future scope, would make the system more useful in
practice.

---

*Source project: [SHADE-IDS](https://github.com/KanishkSigar/shade-ids)*
