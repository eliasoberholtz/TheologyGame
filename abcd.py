import random
from datetime import datetime, timedelta

names = ["John", "Peter", "Paul", "Mark", "Luke", "Matthew", "Andrew", "Thomas", "James", "Philip", "Bartholomew", "Simon", "Jude", "Matthias", "Timothy", "Titus", "Silas", "Barnabas", "Clement", "Ignatius", "Polycarp", "Justin", "Irenaeus", "Origen", "Tertullian", "Cyprian", "Athanasius", "Basil", "Gregory", "Ambrose", "Jerome", "Augustine", "Chrysostom"]

cities = {
    "Alexandria": "Alexandrian",
    "Antioch": "Antiochene",
    "Rome": "Latin",
    "Constantinople": "Neutral",
    "Jerusalem": "Neutral",
    "Carthage": "Latin",
    "Hippo": "Latin",
    "Ephesus": "Neutral",
    "Nicaea": "Neutral",
    "Caesarea": "Antiochene",
    "Edessa": "Antiochene",
    "Milan": "Latin",
    "Ravenna": "Latin",
    "Chalcedon": "Neutral",
    "Tyre": "Antiochene"
}

mentors = {
    "Alexandrian": ["Cyril of Alexandria", "Theophilus of Alexandria", "Dioscorus of Alexandria", "Timothy of Alexandria"],
    "Antiochene": ["Nestorius", "Theodore of Mopsuestia", "John Chrysostom", "Theodoret of Cyrus"],
    "Latin": ["Augustine of Hippo", "Jerome", "Ambrose of Milan", "Pope Celestine I"]
}

mentor_traits = {
    "Cyril of Alexandria": "Persuasive",
    "Theophilus of Alexandria": "Authoritative",
    "Dioscorus of Alexandria": "Ambitious",
    "Timothy of Alexandria": "Diplomatic",
    "Nestorius": "Aggressive",
    "Theodore of Mopsuestia": "Scholarly",
    "John Chrysostom": "Charismatic",
    "Theodoret of Cyrus": "Moderate",
    "Augustine of Hippo": "Philosophical",
    "Jerome": "Erudite",
    "Ambrose of Milan": "Influential",
    "Pope Celestine I": "Authoritative"
}

heresies = ["Arianism", "Nestorianism", "Monophysitism", "Pelagianism", "Donatism"]

patriarchs = {
    "Alexandria": {"name": "Cyril of Alexandria", "death_date": datetime(444, 6, 27)},
    "Antioch": {"name": "John of Antioch", "death_date": datetime(441, 1, 1)},
    "Rome": {"name": "Celestine I", "death_date": datetime(432, 7, 27)},
    "Constantinople": {"name": "Nestorius", "death_date": datetime(451, 1, 1)},
    "Jerusalem": {"name": "Juvenal of Jerusalem", "death_date": datetime(458, 7, 2)}
}

class Theologian:
    def __init__(self):
        self.name = f"{random.choice(names)} of {random.choice(list(cities.keys()))}"
        self.city = self.name.split(" of ")[1]
        self.affiliation = cities[self.city]
        while self.affiliation == "Neutral":
            self.city = random.choice(list(cities.keys()))
            self.affiliation = cities[self.city]
        self.name = f"{self.name.split(' of ')[0]} of {self.city}"
        self.rank = "Priest"
        self.mentor = None
        self.relations = {affiliation: 50 for affiliation in ["Alexandrian", "Antiochene", "Latin"]}
        self.experience = 0
        self.prestige = 0
        self.heresy_suspicion = 0
        self.exiled = False
        self.years_in_exile = 0
        self.is_pope = False
        self.papal_name = None
        self.personal_relations = {}
        self.plotting = False

    def change_affiliation(self, new_affiliation, reason):
        old_affiliation = self.affiliation
        self.affiliation = new_affiliation
        self.relations[old_affiliation] -= 20
        self.relations[new_affiliation] += 20
        print(f"Your affiliation has changed to {new_affiliation} due to {reason}.")

    def promote(self):
        ranks = ["Priest", "Presbyter", "Bishop", "Patriarch"]
        current_index = ranks.index(self.rank)
        if current_index < len(ranks) - 1:
            self.rank = ranks[current_index + 1]
            self.prestige += 25
            print(f"Congratulations! You've been promoted to {self.rank}.")
        else:
            print("You've reached the highest rank possible.")

    def become_patriarch(self):
        self.rank = "Patriarch"
        if self.affiliation == "Latin":
            self.become_pope()

    def become_pope(self):
        self.is_pope = True
        papal_names = ["Leo", "Gregory", "Clement", "Urban", "Innocent", "Benedict", "John", "Pius"]
        self.papal_name = random.choice(papal_names)
        print(f"You have become the Pope! You have chosen the name {self.papal_name}.")

    def update_personal_relation(self, other_theologian, change):
        if other_theologian not in self.personal_relations:
            self.personal_relations[other_theologian] = 50
        self.personal_relations[other_theologian] = max(0, min(100, self.personal_relations[other_theologian] + change))

class Game:
    def __init__(self):
        self.year = 416
        self.quarter = 1
        self.current_date = datetime(416, 1, 1)
        self.player = Theologian()
        self.emperor = "Theodosius II"
        self.emperor_favor = 50
        self.other_theologians = self.generate_theologians()
        self.current_war = None
        self.current_pope = "Celestine I"
        self.synod_topics = [
            "Nature of Christ",
            "Authority of the Pope",
            "Interpretation of Scripture",
            "Role of Mary in Salvation",
            "Predestination and Free Will",
            "Nature of the Trinity",
            "Use of Icons in Worship",
            "Clerical Celibacy",
            "Baptism Practices",
            "Eucharistic Theology"
        ]

    def generate_theologians(self):
        return [Theologian() for _ in range(10)]

    def run(self):
        print(f"Welcome, {self.player.name}!")
        print(f"You are affiliated with the {self.player.affiliation} school.")
        while self.year < 431 or (self.year == 431 and self.quarter < 4):
            self.quarterly_events()
            self.quarter += 1
            if self.quarter > 4:
                self.quarter = 1
                self.year += 1
            self.current_date += timedelta(days=91)  # Roughly a quarter
            self.check_patriarch_deaths()
        self.council_of_ephesus()

    def quarterly_events(self):
        print(f"\nYear: {self.year}, Quarter: {self.quarter}")
        self.display_stats()
        if self.player.exiled:
            self.handle_exile()
            return
        
        self.random_events()
        
        actions = {
            1: ("Study under your mentor", self.study),
            2: ("Write a theological book", self.write_book),
            3: ("Exchange letters with other theologians", self.exchange_letters),
            4: ("Attempt to change affiliation", self.attempt_affiliation_change),
            5: ("Debate your mentor", self.debate_mentor),
            6: ("Seek audience with the Emperor", self.imperial_audience),
            7: ("Do nothing this quarter", lambda: None)
        }
        
        if self.player.rank in ["Patriarch", "Bishop"] or self.player.is_pope:
            actions[8] = ("Call a synod", self.call_synod)
        
        if self.player.rank == "Bishop" and self.player.experience >= 100:
            actions[9] = ("Plot to become Patriarch", self.plot_patriarch)
        
        print("Choose your action for this quarter:")
        for key, value in actions.items():
            print(f"{key}. {value[0]}")
        choice = self.get_input("Enter your choice: ", range(1, len(actions) + 1))
        actions[choice][1]()
        
        self.check_for_synod_invitation()
        self.check_for_heresy()
        self.check_promotion()
        self.update_emperor_favor()

    def display_stats(self):
        print(f"\nStats for {self.player.name}:")
        print(f"Rank: {self.player.rank}")
        print(f"Affiliation: {self.player.affiliation}")
        print(f"Mentor: {self.player.mentor}")
        print(f"Experience: {self.player.experience}")
        print(f"Prestige: {self.player.prestige}")
        print(f"Heresy Suspicion: {self.player.heresy_suspicion}")
        print("Relations:")
        for affiliation, relation in self.player.relations.items():
            print(f"  {affiliation}: {relation}")
        print(f"Emperor's Favor: {self.emperor_favor}")
        if self.player.exiled:
            print(f"Years in Exile: {self.player.years_in_exile}")
        if self.player.is_pope:
            print(f"Papal Name: {self.player.papal_name}")
        print("Personal Relations:")
        for person, relation in self.player.personal_relations.items():
            print(f"  {person}: {relation}")

    def random_events(self):
        if random.random() < 0.01 and not self.current_war:  # 1% chance of war starting
            self.start_war()
        elif self.current_war:
            self.continue_war()
        
        if random.random() < 0.001:  # 0.1% chance of mentor changing affiliation
            self.mentor_affiliation_change()
        
        if random.random() < 0.05 and self.player.mentor is None:  # 5% chance of reconciliation if no mentor
            self.attempt_reconciliation()

    def start_war(self):
        enemies = ["Persians", "Huns", "Visigoths", "Vandals"]
        self.current_war = random.choice(enemies)
        print(f"War has broken out with the {self.current_war}!")
        self.handle_war_effects()

    def continue_war(self):
        print(f"The war with the {self.current_war} continues.")
        self.handle_war_effects()
        if random.random() < 0.2:  # 20% chance of war ending each quarter
            print(f"The war with the {self.current_war} has ended.")
            self.current_war = None

    def handle_war_effects(self):
        print("The ongoing war affects the Church and the Empire.")
        self.emperor_favor += random.randint(-10, 10)
        self.player.prestige += random.randint(-5, 5)

    def mentor_affiliation_change(self):
        if self.player.mentor:
            old_affiliation = next(aff for aff, mentors in mentors.items() if self.player.mentor in mentors)
            new_affiliations = [aff for aff in mentors.keys() if aff != old_affiliation]
            new_affiliation = random.choice(new_affiliations)
            print(f"Shocking news! Your mentor, {self.player.mentor}, has changed affiliation to {new_affiliation}!")
            print("This is a major event that will have significant consequences in the theological world.")
            
            # Update mentor lists
            mentors[old_affiliation].remove(self.player.mentor)
            mentors[new_affiliation].append(self.player.mentor)
            
            # Player decision
            choice = self.get_input("Do you want to: 1. Follow your mentor, 2. Stay with your current affiliation? ", [1, 2])
            if choice == 1:
                self.player.change_affiliation(new_affiliation, f"following your mentor {self.player.mentor}")
            else:
                print(f"You decide to stay with the {self.player.affiliation} school.")
                self.player.mentor = None
                print("You no longer have a mentor.")

    def choose_mentor(self):
        if not self.player.mentor:
            print("Choose a mentor:")
            available_mentors = [mentor for mentor in mentors[self.player.affiliation] 
                                 if mentor not in [p["name"] for p in patriarchs.values()]
                                 and mentor != self.current_pope]
            
            if not available_mentors:
                print("There are no available mentors at this time.")
                return

            for i, mentor in enumerate(available_mentors, 1):
                print(f"{i}. {mentor} - {mentor_traits[mentor]}")
            choice = self.get_input("Enter your choice: ", range(1, len(available_mentors) + 1))
            chosen_mentor = available_mentors[choice - 1]
            self.player.mentor = chosen_mentor
            
            print(f"You are now studying under {self.player.mentor}.")

    def study(self):
        if not self.player.mentor:
            self.choose_mentor()
        if self.player.mentor:
            print(f"You study under {self.player.mentor}.")
            trait = mentor_traits[self.player.mentor]
            self.player.experience += random.randint(5, 15)
            self.player.update_personal_relation(self.player.mentor, random.randint(1, 5))
        else:
            print("You study on your own.")
            self.player.experience += random.randint(3, 10)

    def write_book(self):
        print("You've written a theological book.")
        self.player.prestige += random.randint(5, 15)
        self.player.experience += random.randint(10, 20)
        self.player.heresy_suspicion += random.randint(0, 5)

    def call_synod(self):
        print("You've called a synod. This increases your prestige but may affect your relations.")
        self.player.prestige += random.randint(10, 30)
        topic = random.choice(self.synod_topics)
        print(f"The synod will focus on: {topic}")
        
        attendees = self.generate_synod_attendees()
        for attendee in attendees:
            if attendee != self.player.name:
                self.player.update_personal_relation(attendee, random.randint(-5, 5))
        
        print("The synod begins with a series of debates:")
        for _ in range(3):
            debater1, debater2 = random.sample(attendees, 2)
            print(f"{debater1} debates against {debater2}")
            winner = random.choice([debater1, debater2])
            print(f"{winner} makes a compelling argument!")
        
        print("\nThe synod is drafting canons. You can speak for or against them:")
        for _ in range(3):
            canon = self.generate_canon(topic)
            print(f"Proposed Canon: {canon}")
            choice = self.get_input("Do you want to: 1. Support, 2. Oppose, 3. Remain neutral? ", [1, 2, 3])
            if choice == 1:
                print("You speak in favor of the canon.")
                self.player.prestige += random.randint(5, 15)
            elif choice == 2:
                print("You speak against the canon.")
                self.player.prestige += random.randint(5, 15)
                self.player.heresy_suspicion += random.randint(0, 5)
            else:
                print("You remain neutral.")
        
        print("The synod concludes. Your actions have affected your relations with other theologians.")

    def generate_synod_attendees(self):
        attendees = [self.player.name]
        attendees.extend(random.sample([t.name for t in self.other_theologians], 5))
        return attendees

    def generate_canon(self, topic):
        canons = {
            "Nature of Christ": [
                "Christ has two natures, divine and human, in one hypostasis (person)",
                "The Logos has a single nature, the divine nature incarnate",
                "Christ's natures are distinct in their properties, but united in one person",
                "The divine and human natures in Christ are united without confusion, change, division, or separation"
            ],
            "Authority of the Pope": [
                "The Bishop of Rome holds primacy among all bishops",
                "The authority of the Pope is derived from apostolic succession through Peter",
                "Ecumenical councils require papal approval to be valid",
                "The Pope's authority is equal to that of other Patriarchs in their respective sees"
            ],
            "Interpretation of Scripture": [
                "Scripture should be interpreted primarily in its literal sense",
                "The allegorical interpretation of Scripture reveals deeper spiritual truths",
                "The Church Fathers' interpretations should guide our understanding of Scripture",
                "Scripture interpretation requires both literal and spiritual understanding, guided by tradition"
            ],
            "Role of Mary in Salvation": [
                "Mary is the Theotokos (God-bearer), emphasizing Christ's divinity",
                "Mary is the Christotokos (Christ-bearer), emphasizing Christ's humanity",
                "Mary's perpetual virginity is a dogma of the faith",
                "Mary, as the New Eve, plays a cooperative role in salvation history"
            ],
            "Predestination and Free Will": [
                "God predestines the elect to salvation, while others are left to their just condemnation",
                "God's grace is necessary for salvation, but humans have free will to accept or reject it",
                "Predestination is based on God's foreknowledge of human choices",
                "Salvation is a synergy between divine grace and human free will"
            ],
            "Nature of the Trinity": [
                "The Father, Son, and Holy Spirit are consubstantial and co-eternal",
                "The Holy Spirit proceeds from the Father alone",
                "The Holy Spirit proceeds from the Father and the Son",
                "The three Persons of the Trinity are distinct but inseparable in their one divine essence"
            ],
            "Use of Icons in Worship": [
                "Icons are windows to heaven and should be venerated",
                "The use of icons in worship constitutes idolatry and should be forbidden",
                "Icons are permissible as educational tools but should not be venerated",
                "The veneration of icons is directed to the prototype, not the material image"
            ],
            "Clerical Celibacy": [
                "All clergy should practice celibacy to fully devote themselves to God",
                "Married men may be ordained, but must remain celibate after ordination",
                "Clergy may marry before ordination to the diaconate or priesthood, but not after",
                "Celibacy should be a personal choice for clergy, not a mandatory rule"
            ],
            "Baptism Practices": [
                "Baptism should be administered by triple immersion in the name of the Trinity",
                "Infant baptism is necessary for salvation and should be practiced",
                "Only believers' baptism (of adults) is valid and should be practiced",
                "The form of baptism (immersion, pouring, or sprinkling) is not essential to its validity"
            ],
            "Eucharistic Theology": [
                "The bread and wine truly become the Body and Blood of Christ in substance",
                "Christ is spiritually present in the Eucharist, but the elements do not change",
                "The Eucharist is a memorial of Christ's sacrifice, not a re-presentation",
                "The change in the Eucharistic elements occurs through the epiclesis (invocation of the Holy Spirit)"
            ]
        }
        return random.choice(canons.get(topic, ["A general canon about church governance"]))

    def check_for_synod_invitation(self):
        if self.player.rank in ["Presbyter", "Bishop", "Patriarch"] and random.random() < 0.2:
            print("You have been invited to attend a synod.")
            self.attend_synod()

    def attend_synod(self):
        print("You're attending a synod. Your actions here can affect your relations and prestige.")
        choice = self.get_input("How do you want to act? (1: Assertive, 2: Diplomatic, 3: Neutral): ", [1, 2, 3])
        if choice == 1:
            print("You assert your views strongly.")
            self.player.prestige += random.randint(10, 20)
            for affiliation in self.player.relations:
                if affiliation != self.player.affiliation:
                    self.player.relations[affiliation] -= random.randint(10, 20)
        elif choice == 2:
            print("You take a diplomatic approach.")
            self.player.prestige += random.randint(5, 15)
            for affiliation in self.player.relations:
                self.player.relations[affiliation] += random.randint(5, 15)
        else:
            print("You remain neutral.")
            self.player.prestige += random.randint(0, 5)
        
        if self.player.rank == "Patriarch" or self.player.is_pope:
            self.handle_patriarch_powers()

    def handle_patriarch_powers(self):
        if self.player.is_pope:
            print("As the Pope, you have the power to nullify any canon of this synod.")
        else:
            print("As a Patriarch, you have the power to nullify any canon of this synod.")
        
        choice = self.get_input("Do you want to nullify any canons? (1: Yes, 2: No): ", [1, 2])
        if choice == 1:
            print("You nullify a controversial canon. This increases your prestige but may affect your relations.")
            self.player.prestige += random.randint(20, 40)
            for affiliation in self.player.relations:
                if affiliation != self.player.affiliation:
                    self.player.relations[affiliation] -= random.randint(10, 30)

    def exchange_letters(self):
        other_theologian = random.choice(self.other_theologians)
        print(f"You exchange letters with {other_theologian.name}.")
        if random.random() < 0.6:
            print("The exchange is fruitful and increases your understanding.")
            self.player.experience += random.randint(5, 10)
            self.player.relations[other_theologian.affiliation] += random.randint(5, 10)
            self.player.update_personal_relation(other_theologian.name, random.randint(5, 15))
        else:
            print("The exchange leads to a theological disagreement.")
            self.player.relations[other_theologian.affiliation] -= random.randint(5, 10)
            self.player.heresy_suspicion += random.randint(0, 5)
            self.player.update_personal_relation(other_theologian.name, random.randint(-15, -5))

    def attempt_affiliation_change(self):
        current_affiliation = self.player.affiliation
        possible_affiliations = [aff for aff in ["Alexandrian", "Antiochene", "Latin"] if aff != current_affiliation]
        print("Choose an affiliation to attempt to join:")
        for i, aff in enumerate(possible_affiliations, 1):
            print(f"{i}. {aff}")
        choice = self.get_input("Enter your choice: ", range(1, len(possible_affiliations) + 1))
        new_affiliation = possible_affiliations[choice - 1]
        if random.random() < 0.5:
            self.player.change_affiliation(new_affiliation, "personal decision")
            self.player.mentor = None  # Reset mentor when changing affiliation
        else:
            print(f"Your attempt to join the {new_affiliation} school was unsuccessful.")
            self.player.relations[new_affiliation] -= random.randint(5, 15)

    def debate_mentor(self):
        if not self.player.mentor:
            print("You don't have a mentor to debate with.")
            return
        print(f"You challenge your mentor, {self.player.mentor}, to a theological debate.")
        debate_skill = random.randint(1, 100) + self.player.prestige // 10
        mentor_skill = random.randint(50, 150)
        if debate_skill > mentor_skill:
            print("You win the debate!")
            self.player.prestige += random.randint(20, 40)
            self.player.update_personal_relation(self.player.mentor, random.randint(5, 15))
            if random.random() < 0.2:
                print(f"{self.player.mentor} is impressed and promotes you!")
                self.player.promote()
        elif debate_skill < mentor_skill - 30:
            print("You lose the debate badly.")
            print(f"{self.player.mentor} abandons you as a student.")
            self.player.update_personal_relation(self.player.mentor, random.randint(-30, -20))
            self.player.mentor = None
            self.player.prestige -= random.randint(10, 30)
        else:
            print("The debate is inconclusive.")
            self.player.prestige += random.randint(5, 15)
            self.player.update_personal_relation(self.player.mentor, random.randint(-5, 5))

    def imperial_audience(self):
        print("You seek an audience with Emperor", self.emperor)
        if random.random() < self.emperor_favor / 100:
            print("The Emperor grants you an audience.")
            choice = self.get_input("How do you approach the Emperor? (1: Flatter, 2: Discuss theology, 3: Request favor): ", [1, 2, 3])
            if choice == 1:
                print("You flatter the Emperor.")
                self.emperor_favor += random.randint(5, 15)
            elif choice == 2:
                print("You engage in a theological discussion with the Emperor.")
                if random.random() < 0.5:
                    print("The Emperor is impressed by your knowledge.")
                    self.emperor_favor += random.randint(10, 20)
                    self.player.prestige += random.randint(5, 15)
                else:
                    print("The Emperor disagrees with your views.")
                    self.emperor_favor -= random.randint(5, 15)
            else:
                print("You request a favor from the Emperor.")
                if random.random() < 0.3:
                    print("The Emperor grants your request.")
                    self.player.prestige += random.randint(10, 30)
                else:
                    print("The Emperor denies your request.")
                    self.emperor_favor -= random.randint(5, 15)
        else:
            print("The Emperor declines to see you.")
            self.emperor_favor -= random.randint(1, 5)

    def check_for_heresy(self):
        if random.random() < self.player.heresy_suspicion / 100:
            heresy = random.choice(heresies)
            print(f"You have been accused of {heresy}!")
            if self.player.prestige > 50 and random.random() < 0.5:
                print("However, your prestige and connections protect you from serious consequences.")
                self.player.prestige -= random.randint(10, 20)
            else:
                print("You are condemned as a heretic.")
                self.handle_condemnation()

    def handle_condemnation(self):
        if random.random() < self.emperor_favor / 100:
            print("The Emperor intervenes on your behalf, mitigating your punishment.")
            self.player.prestige -= random.randint(20, 40)
        elif random.random() < 0.5:
            print("You are exiled.")
            self.player.exiled = True
            self.player.years_in_exile = 0
        else:
            print("You are excommunicated and exiled.")
            self.player.exiled = True
            self.player.years_in_exile = 0
            self.player.prestige = 0

    def handle_exile(self):
        self.player.years_in_exile += 1
        print(f"You are in exile. Years in exile: {self.player.years_in_exile}")
        if self.player.years_in_exile >= 3 and random.random() < 0.3:
            print("You have been allowed to return from exile!")
            self.player.exiled = False
            self.player.years_in_exile = 0
            self.player.prestige += random.randint(10, 30)
        elif random.random() < 0.1:
            print("You die in exile. Game Over.")
            self.end_game()

    def update_emperor_favor(self):
        change = random.randint(-5, 5)
        self.emperor_favor = max(0, min(100, self.emperor_favor + change))

    def check_promotion(self):
        if self.player.experience >= 100:
            old_rank = self.player.rank
            if old_rank != "Bishop":
                self.player.promote()
                self.player.experience = 0
            elif old_rank == "Bishop":
                print("You have gained enough experience to be considered for the role of Patriarch.")
                print("You can now plot to become Patriarch or wait for the current Patriarch to die.")

    def plot_patriarch(self):
        if self.player.plotting:
            print("You are already plotting to become Patriarch.")
            return
        self.player.plotting = True
        print("You begin plotting to become the Patriarch.")
        self.player.prestige -= random.randint(5, 15)
        self.player.heresy_suspicion += random.randint(5, 15)
        if random.random() < 0.2:
            print("Your plot is successful! The current Patriarch is deposed.")
            self.become_patriarch()
        else:
            print("Your plot fails. Your reputation suffers.")
            self.player.prestige -= random.randint(20, 40)
            self.player.heresy_suspicion += random.randint(10, 30)
        self.player.plotting = False

    def become_patriarch(self):
        print("A new Patriarch must be chosen.")
        debate_skill = random.randint(1, 100) + self.player.prestige // 10
        opponent_skill = random.randint(50, 150)
        print("You make your case to be chosen as the new Patriarch.")
        if debate_skill > opponent_skill:
            print("Your arguments are persuasive. You are chosen as the new Patriarch!")
            self.player.become_patriarch()
            self.player.prestige += random.randint(50, 100)
            patriarchs[self.player.city]["name"] = self.player.name if not self.player.is_pope else self.player.papal_name
            patriarchs[self.player.city]["death_date"] = self.current_date + timedelta(days=random.randint(365*5, 365*20))
            if self.player.is_pope:
                self.current_pope = self.player.papal_name
        else:
            print("Despite your efforts, another candidate is chosen as Patriarch.")
            self.player.prestige -= random.randint(10, 30)

    def check_patriarch_deaths(self):
        for city, patriarch in patriarchs.items():
            if self.current_date >= patriarch["death_date"]:
                print(f"{patriarch['name']}, the Patriarch of {city}, has died.")
                if city == self.player.city and self.player.rank == "Bishop":
                    self.become_patriarch()
                else:
                    new_patriarch = f"{random.choice(names)} of {city}"
                    patriarchs[city]["name"] = new_patriarch
                    patriarchs[city]["death_date"] = self.current_date + timedelta(days=random.randint(365*5, 365*20))
                    print(f"{new_patriarch} has been chosen as the new Patriarch of {city}.")
                    if city == "Rome":
                        self.current_pope = new_patriarch
                
                # Remove the deceased patriarch from mentors if they were one
                for school, mentor_list in mentors.items():
                    if patriarch["name"] in mentor_list:
                        mentor_list.remove(patriarch["name"])
                        print(f"{patriarch['name']} is no longer available as a mentor.")
                
                # If the player's mentor was the deceased patriarch, remove them
                if self.player.mentor == patriarch["name"]:
                    print(f"Your mentor, {self.player.mentor}, has passed away.")
                    self.player.mentor = None

    def attempt_reconciliation(self):
        past_mentors = [mentor for mentor, relation in self.player.personal_relations.items() if relation < 50 and mentor in [m for sublist in mentors.values() for m in sublist]]
        if past_mentors:
            reconciling_mentor = random.choice(past_mentors)
            print(f"{reconciling_mentor} reaches out to you, seeking reconciliation.")
            choice = self.get_input("Do you accept? 1. Yes, 2. No ", [1, 2])
            if choice == 1:
                print(f"You reconcile with {reconciling_mentor}. They become your mentor again.")
                self.player.mentor = reconciling_mentor
                self.player.update_personal_relation(reconciling_mentor, random.randint(20, 40))
            else:
                print("You decline the reconciliation.")
                self.player.update_personal_relation(reconciling_mentor, random.randint(-10, -5))

    def council_of_ephesus(self):
        print("\nThe Council of Ephesus has begun!")
        print("This is the culmination of years of theological debate.")
        
        influence = self.player.prestige + self.player.relations["Antiochene"] - self.player.relations["Alexandrian"]
        if self.player.is_pope:
            influence += 100
        elif self.player.rank == "Patriarch":
            influence += 50
        elif self.player.rank == "Bishop":
            influence += 25

        if self.player.is_pope:
            print("As the Pope, you have significant influence over the council.")
            choice = self.get_input("How do you want to steer the council? (1: Support Cyril, 2: Support Nestorius, 3: Remain neutral): ", [1, 2, 3])
            if choice == 1:
                print("You decisively support Cyril of Alexandria's position.")
                influence -= 100
            elif choice == 2:
                print("You decisively support Nestorius's position.")
                influence += 100
            else:
                print("You maintain a neutral stance, allowing the debate to unfold naturally.")
        else:
            choice = self.get_input("How do you want to approach the council? (1: Support Cyril, 2: Support Nestorius, 3: Remain neutral): ", [1, 2, 3])
            if choice == 1:
                print("You support Cyril of Alexandria's position.")
                influence -= 50
            elif choice == 2:
                print("You support Nestorius's position.")
                influence += 50
            else:
                print("You remain neutral in the debate.")

        if influence > 100:
            print("Through your influence and arguments, Nestorius is not condemned!")
            print("This is a major upset and will have significant consequences for the Church.")
            if self.player.affiliation == "Antiochene":
                self.player.prestige += 100
            else:
                self.player.prestige += 50
        else:
            print("The council concludes with the condemnation of Nestorius.")
            if self.player.affiliation == "Antiochene":
                print("As an Antiochene, this outcome is unfavorable for you.")
                self.player.prestige -= 20
            elif self.player.affiliation == "Alexandrian":
                print("As an Alexandrian, this outcome is favorable for you.")
                self.player.prestige += 20
        
        self.end_game()

    def end_game(self):
        print("\nGame Over!")
        self.display_stats()
        if self.player.prestige >= 200 and self.player.rank == "Patriarch":
            print("Congratulations! You've become a highly influential figure in the Church!")
        elif self.player.prestige >= 100:
            print("You've made a name for yourself in theological circles.")
        else:
            print("Your influence in the Church remains limited.")
        exit()

    def get_input(self, prompt, options):
        while True:
            try:
                choice = int(input(prompt))
                if choice in options:
                    return choice
                print("Invalid input. Please try again.")
            except ValueError:
                print("Please enter a number.")

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()


