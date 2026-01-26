CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE (p.name) IS UNIQUE;
CREATE INDEX IF NOT EXISTS FOR (p:Person) ON (p.gender);

CREATE (Brahma:Person {name: 'Brahma', gender: 'Male'})
CREATE (Marichi:Person {name: 'Marichi', gender: 'Male'})
CREATE (Brahma)-[:FATHER_OF]->(Marichi)
CREATE (Marichi)-[:SON_OF]->(Brahma)
CREATE (Kala:Person {name: 'Kala', gender: 'Female'})
CREATE (Marichi)-[:HUSBAND_OF]->(Kala)
CREATE (Kala)-[:WIFE_OF]->(Marichi)
CREATE (Kashyapa:Person {name: 'Kashyapa', gender: 'Male', type: 'sage'})
CREATE (Marichi)-[:FATHER_OF]->(Kashyapa)
CREATE (Kala)-[:MOTHER_OF]->(Kashyapa)
CREATE (Kashyapa)-[:SON_OF]->(Marichi)
CREATE (Kashyapa)-[:SON_OF]->(Kala)

CREATE (DakshaPrajapati:Person {name: 'Daksha Prajapati', gender: 'Male'})
CREATE (Brahma)-[:FATHER_OF]->(DakshaPrajapati)
CREATE (DakshaPrajapati)-[:SON_OF]->(Brahma)
CREATE (Aditi:Person {name: 'Aditi', gender: 'Female'})
CREATE (Diti:Person {name: 'Diti', gender: 'Female'})
CREATE (Danu:Person {name: 'Danu', gender: 'Female'})
CREATE (Arishta:Person {name: 'Arishta', gender: 'Female'})
CREATE (Surasa:Person {name: 'Surasa', gender: 'Female'})
CREATE (Khasa:Person {name: 'Khasa', gender: 'Female'})
CREATE (Surabhi:Person {name: 'Surabhi', gender: 'Female'})
CREATE (Vinata:Person {name: 'Vinata', gender: 'Female'})
CREATE (Tamra:Person {name: 'Tamra', gender: 'Female'})
CREATE (Krodhavasha:Person {name: 'Krodhavasha', gender: 'Female'})
CREATE (Ila:Person {name: 'Ila', gender: 'Female'})
CREATE (Kadru:Person {name: 'Kadru', gender: 'Female'})
CREATE (Muni:Person {name: 'Muni', gender: 'Female'})

CREATE 
(DakshaPrajapati)-[:FATHER_OF]->(Aditi),
(DakshaPrajapati)-[:FATHER_OF]->(Diti),
(DakshaPrajapati)-[:FATHER_OF]->(Danu),
(DakshaPrajapati)-[:FATHER_OF]->(Arishta),
(DakshaPrajapati)-[:FATHER_OF]->(Surasa),
(DakshaPrajapati)-[:FATHER_OF]->(Khasa),
(DakshaPrajapati)-[:FATHER_OF]->(Surabhi),
(DakshaPrajapati)-[:FATHER_OF]->(Vinata),
(DakshaPrajapati)-[:FATHER_OF]->(Tamra),
(DakshaPrajapati)-[:FATHER_OF]->(Krodhavasha),
(DakshaPrajapati)-[:FATHER_OF]->(Ila),
(DakshaPrajapati)-[:FATHER_OF]->(Kadru),
(DakshaPrajapati)-[:FATHER_OF]->(Muni)

CREATE 
(Aditi)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Diti)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Danu)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Arishta)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Surasa)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Khasa)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Surabhi)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Vinata)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Tamra)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Krodhavasha)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Ila)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Kadru)-[:DAUGHTER_OF]->(DakshaPrajapati),
(Muni)-[:DAUGHTER_OF]->(DakshaPrajapati)

CREATE 
(Kashyapa)-[:HUSBAND_OF]->(Aditi),
(Kashyapa)-[:HUSBAND_OF]->(Diti),
(Kashyapa)-[:HUSBAND_OF]->(Danu),
(Kashyapa)-[:HUSBAND_OF]->(Arishta),
(Kashyapa)-[:HUSBAND_OF]->(Surasa),
(Kashyapa)-[:HUSBAND_OF]->(Khasa),
(Kashyapa)-[:HUSBAND_OF]->(Surabhi),
(Kashyapa)-[:HUSBAND_OF]->(Vinata),
(Kashyapa)-[:HUSBAND_OF]->(Tamra),
(Kashyapa)-[:HUSBAND_OF]->(Krodhavasha),
(Kashyapa)-[:HUSBAND_OF]->(Ila),
(Kashyapa)-[:HUSBAND_OF]->(Kadru),
(Kashyapa)-[:HUSBAND_OF]->(Muni)


CREATE 
(Aditi)-[:WIFE_OF]->(Kashyapa),
(Diti)-[:WIFE_OF]->(Kashyapa),
(Danu)-[:WIFE_OF]->(Kashyapa),
(Arishta)-[:WIFE_OF]->(Kashyapa),
(Surasa)-[:WIFE_OF]->(Kashyapa),
(Khasa)-[:WIFE_OF]->(Kashyapa),
(Surabhi)-[:WIFE_OF]->(Kashyapa),
(Vinata)-[:WIFE_OF]->(Kashyapa),
(Tamra)-[:WIFE_OF]->(Kashyapa),
(Krodhavasha)-[:WIFE_OF]->(Kashyapa),
(Ila)-[:WIFE_OF]->(Kashyapa),
(Kadru)-[:WIFE_OF]->(Kashyapa),
(Muni)-[:WIFE_OF]->(Kashyapa)


CREATE (Vishnu:Person {name: 'Vishnu', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Shakra:Person {name: 'Shakra', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Aryama:Person {name: 'Aryama', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Dhata:Person {name: 'Dhata', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Vidhata:Person {name: 'Vidhata', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Tvashta:Person {name: 'Tvashta', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Pusha:Person {name: 'Pusha', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Vivasvana:Person {name: 'Vivasvana', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Savita:Person {name: 'Savita', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Mitravaruna:Person {name: 'Mitravaruna', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Amsha:Person {name: 'Amsha', gender: 'Male', type: 'Aditya', dynasty: 'solar'})
CREATE (Bhaga:Person {name: 'Bhaga', gender: 'Male', type: 'Aditya', dynasty: 'solar'})

CREATE 
(Kashyapa)-[:FATHER_OF]->(Vishnu),
(Kashyapa)-[:FATHER_OF]->(Shakra),
(Kashyapa)-[:FATHER_OF]->(Aryama),
(Kashyapa)-[:FATHER_OF]->(Dhata),
(Kashyapa)-[:FATHER_OF]->(Vidhata),
(Kashyapa)-[:FATHER_OF]->(Tvashta),
(Kashyapa)-[:FATHER_OF]->(Pusha),
(Kashyapa)-[:FATHER_OF]->(Vivasvana),
(Kashyapa)-[:FATHER_OF]->(Savita),
(Kashyapa)-[:FATHER_OF]->(Mitravaruna),
(Kashyapa)-[:FATHER_OF]->(Amsha),
(Kashyapa)-[:FATHER_OF]->(Bhaga)


CREATE 
(Aditi)-[:MOTHER_OF]->(Vishnu),
(Aditi)-[:MOTHER_OF]->(Shakra),
(Aditi)-[:MOTHER_OF]->(Aryama),
(Aditi)-[:MOTHER_OF]->(Dhata),
(Aditi)-[:MOTHER_OF]->(Vidhata),
(Aditi)-[:MOTHER_OF]->(Tvashta),
(Aditi)-[:MOTHER_OF]->(Pusha),
(Aditi)-[:MOTHER_OF]->(Vivasvana),
(Aditi)-[:MOTHER_OF]->(Savita),
(Aditi)-[:MOTHER_OF]->(Mitravaruna),
(Aditi)-[:MOTHER_OF]->(Amsha),
(Aditi)-[:MOTHER_OF]->(Bhaga)


CREATE 
(Vishnu)-[:SON_OF]->(Kashyapa),
(Shakra)-[:SON_OF]->(Kashyapa),
(Aryama)-[:SON_OF]->(Kashyapa),
(Dhata)-[:SON_OF]->(Kashyapa),
(Vidhata)-[:SON_OF]->(Kashyapa),
(Tvashta)-[:SON_OF]->(Kashyapa),
(Pusha)-[:SON_OF]->(Kashyapa),
(Vivasvana)-[:SON_OF]->(Kashyapa),
(Savita)-[:SON_OF]->(Kashyapa),
(Mitravaruna)-[:SON_OF]->(Kashyapa),
(Amsha)-[:SON_OF]->(Kashyapa),
(Bhaga)-[:SON_OF]->(Kashyapa)


CREATE 
(Vishnu)-[:SON_OF]->(Aditi),
(Shakra)-[:SON_OF]->(Aditi),
(Aryama)-[:SON_OF]->(Aditi),
(Dhata)-[:SON_OF]->(Aditi),
(Vidhata)-[:SON_OF]->(Aditi),
(Tvashta)-[:SON_OF]->(Aditi),
(Pusha)-[:SON_OF]->(Aditi),
(Vivasvana)-[:SON_OF]->(Aditi),
(Savita)-[:SON_OF]->(Aditi),
(Mitravaruna)-[:SON_OF]->(Aditi),
(Amsha)-[:SON_OF]->(Aditi),
(Bhaga)-[:SON_OF]->(Aditi)


CREATE (Hiranyakshyapu:Person {name: 'Hiranyakshyapu', gender: 'Male', type: 'Daitya'})
CREATE (Hiranyaksha:Person {name: 'Hiranyaksha', gender: 'Male', type: 'Daitya'})
CREATE (Maruts:Person {name: 'Maruts', gender: 'Male', count: '49'})
CREATE (Simhika:Person {name: 'Simhika', gender: 'Female'})
CREATE (Viprachitti:Person {name: 'Viprachitti', gender: 'Male', type: 'Danava'})

CREATE 
(Kashyapa)-[:FATHER_OF]->(Hiranyakshyapu),
(Kashyapa)-[:FATHER_OF]->(Hiranyaksha)

CREATE 
(Diti)-[:MOTHER_OF]->(Hiranyakshyapu),
(Diti)-[:MOTHER_OF]->(Hiranyaksha),
(Diti)-[:MOTHER_OF]->(Maruts),
(Diti)-[:MOTHER_OF]->(Simhika)

CREATE
(Hiranyakshyapu)-[:SON_OF]->(Kashyapa),
(Hiranyaksha)-[:SON_OF]->(Kashyapa)


CREATE 
(Hiranyakshyapu)-[:SON_OF]->(Diti),
(Hiranyaksha)-[:SON_OF]->(Diti),
(Maruts)-[:SON_OF]->(Diti),
(Simhika)-[:DAUGHTER_OF]->(Diti)

CREATE 
(Viprachitti)-[:HUSBAND_OF]->(Simhika),
(Simhika)-[:WIFE_OF]->(Viprachitti)

CREATE (Danavas:Person {name: 'Danavas', gender: 'Male', count: '100', type: 'Danava'})
CREATE (Danu)-[:MOTHER_OF]->(Danavas)
CREATE (Danavas)-[:SON_OF]->(Danu)


CREATE (Gandharvas:Person {name: 'Gandharvas', gender: 'Male', type: 'Singers'})
CREATE 
(Arishta)-[:MOTHER_OF]->(Gandharvas),
(Kashyapa)-[:FATHER_OF]->(Gandharvas)

CREATE 
(Gandharvas)-[:SON_OF]->(Arishta),
(Gandharvas)-[:SON_OF]->(Kashyapa)


CREATE (Saranyu:Person {name:'Saranyu', gender: 'Female'})
CREATE (SwambhuvaManu:Person {name:'Swambhuva Manu', gender: 'Male', nickname: 'Manu', type: 'First Man on Earth'})
CREATE
(Vivasvana)-[:HUSBAND_OF]->(Saranyu),
(Saranyu)-[:WIFE_OF]->(Vivasvana),
(Vivasvana)-[:FATHER_OF]->(SwambhuvaManu),
(Saranyu)-[:MOTHER_OF]->(SwambhuvaManu),
(SwambhuvaManu)-[:SON_OF]->(Vivasvana),
(SwambhuvaManu)-[:SON_OF]->(Saranyu)


CREATE (Shraddha:Person {name:'Shraddha', gender: 'Female'})
CREATE (DeviIla:Person {name:'Devi Ila', gender: 'Female', nickname: 'Ila'})
CREATE
(SwambhuvaManu)-[:HUSBAND_OF]->(Shraddha),
(Shraddha)-[:WIFE_OF]->(SwambhuvaManu),
(SwambhuvaManu)-[:FATHER_OF]->(DeviIla),
(Shraddha)-[:MOTHER_OF]->(DeviIla),
(DeviIla)-[:DAUGHTER_OF]->(SwambhuvaManu),
(DeviIla)-[:DAUGHTER_OF]->(Shraddha)


CREATE (Budha:Person {name:'Budha', gender: 'Male'})
CREATE (Pururava:Person {name:'Pururava', gender: 'Male'})
CREATE
(Budha)-[:HUSBAND_OF]->(DeviIla),
(DeviIla)-[:WIFE_OF]->(Budha),
(Budha)-[:FATHER_OF]->(Pururava),
(DeviIla)-[:MOTHER_OF]->(Pururava),
(Pururava)-[:SON_OF]->(Budha),
(Pururava)-[:SON_OF]->(DeviIla)


CREATE (Uravashi:Person {name:'Uravashi', gender: 'Female', type: 'Apasara'})
CREATE (Ayu:Person {name:'Ayu', gender: 'Male'})
CREATE
(Pururava)-[:HUSBAND_OF]->(Uravashi),
(Uravashi)-[:WIFE_OF]->(Pururava),
(Pururava)-[:FATHER_OF]->(Ayu),
(Uravashi)-[:MOTHER_OF]->(Ayu),
(Ayu)-[:SON_OF]->(Pururava),
(Ayu)-[:SON_OF]->(Uravashi)


CREATE (Prabha:Person {name:'Prabha', gender: 'Female'})
CREATE (Nahusha:Person {name:'Nahusha', gender: 'Male'})
CREATE
(Ayu)-[:HUSBAND_OF]->(Prabha),
(Prabha)-[:WIFE_OF]->(Ayu),
(Ayu)-[:FATHER_OF]->(Nahusha),
(Prabha)-[:MOTHER_OF]->(Nahusha),
(Nahusha)-[:SON_OF]->(Ayu),
(Nahusha)-[:SON_OF]->(Prabha)


CREATE (Ashokasundari:Person {name:'Ashokasundari', gender: 'Female', nickname:'Viraja'})
CREATE (LordShiva:Person {name:'Lord Shiva', gender: 'Male'})
CREATE (Yayati:Person {name:'Yayati', gender: 'Male'})
CREATE
(LordShiva)-[:FATHER_OF]->(Ashokasundari),
(Ashokasundari)-[:DAUGHTER_OF]->(LordShiva),
(Nahusha)-[:HUSBAND_OF]->(Ashokasundari),
(Ashokasundari)-[:WIFE_OF]->(Nahusha),
(Nahusha)-[:FATHER_OF]->(Yayati),
(Ashokasundari)-[:MOTHER_OF]->(Yayati),
(Yayati)-[:SON_OF]->(Nahusha),
(Yayati)-[:SON_OF]->(Ashokasundari)


CREATE (Sarmishtha:Person {name:'Sarmishtha', gender: 'Female'})
CREATE (Puru:Person {name:'Puru', gender: 'Male'})
CREATE
(Yayati)-[:HUSBAND_OF]->(Sarmishtha),
(Sarmishtha)-[:WIFE_OF]->(Yayati),
(Yayati)-[:FATHER_OF]->(Puru),
(Sarmishtha)-[:MOTHER_OF]->(Puru),
(Puru)-[:SON_OF]->(Yayati),
(Puru)-[:SON_OF]->(Sarmishtha)


CREATE (Kaushalya:Person {name:'Kaushalya', gender: 'Female'})
CREATE (JanamejayaI:Person {name:'Janamejaya (I)', gender: 'Male'})
CREATE
(Puru)-[:HUSBAND_OF]->(Kaushalya),
(Kaushalya)-[:WIFE_OF]->(Puru),
(Puru)-[:FATHER_OF]->(JanamejayaI),
(Kaushalya)-[:MOTHER_OF]->(JanamejayaI),
(JanamejayaI)-[:SON_OF]->(Puru),
(JanamejayaI)-[:SON_OF]->(Kaushalya)


CREATE (Ananta:Person {name:'Ananta', gender: 'Female'})
CREATE (Pranchinvan:Person {name:'Pranchinvan', gender: 'Male'})
CREATE
(JanamejayaI)-[:HUSBAND_OF]->(Ananta),
(Ananta)-[:WIFE_OF]->(JanamejayaI),
(JanamejayaI)-[:FATHER_OF]->(Pranchinvan),
(Ananta)-[:MOTHER_OF]->(Pranchinvan),
(Pranchinvan)-[:SON_OF]->(JanamejayaI),
(Pranchinvan)-[:SON_OF]->(Ananta)


CREATE (Asmaki:Person {name:'Asmaki', gender: 'Female'})
CREATE (Sanyati:Person {name:'Sanyati', gender: 'Male'})
CREATE
(Pranchinvan)-[:HUSBAND_OF]->(Asmaki),
(Asmaki)-[:WIFE_OF]->(Pranchinvan),
(Pranchinvan)-[:FATHER_OF]->(Sanyati),
(Asmaki)-[:MOTHER_OF]->(Sanyati),
(Sanyati)-[:SON_OF]->(Pranchinvan),
(Sanyati)-[:SON_OF]->(Asmaki)


CREATE (Varangi:Person {name:'Varangi', gender: 'Female'})
CREATE (Ahamyati:Person {name:'Ahamyati', gender: 'Male'})
CREATE
(Sanyati)-[:HUSBAND_OF]->(Varangi),
(Varangi)-[:WIFE_OF]->(Sanyati),
(Sanyati)-[:FATHER_OF]->(Ahamyati),
(Varangi)-[:MOTHER_OF]->(Ahamyati),
(Ahamyati)-[:SON_OF]->(Sanyati),
(Ahamyati)-[:SON_OF]->(Varangi)


CREATE (Bhanumati:Person {name:'Bhanumati', gender: 'Female'})
CREATE (Sarvabhauma:Person {name:'Sarvabhauma', gender: 'Male'})
CREATE
(Ahamyati)-[:HUSBAND_OF]->(Bhanumati),
(Bhanumati)-[:WIFE_OF]->(Ahamyati),
(Ahamyati)-[:FATHER_OF]->(Sarvabhauma),
(Bhanumati)-[:MOTHER_OF]->(Sarvabhauma),
(Sarvabhauma)-[:SON_OF]->(Ahamyati),
(Sarvabhauma)-[:SON_OF]->(Bhanumati)


CREATE (SunandaI:Person {name:'Sunanda (I)', gender: 'Female'})
CREATE (Jayatsen:Person {name:'Jayatsen', gender: 'Male'})
CREATE
(Sarvabhauma)-[:HUSBAND_OF]->(SunandaI),
(SunandaI)-[:WIFE_OF]->(Sarvabhauma),
(Sarvabhauma)-[:FATHER_OF]->(Jayatsen),
(SunandaI)-[:MOTHER_OF]->(Jayatsen),
(Jayatsen)-[:SON_OF]->(Sarvabhauma),
(Jayatsen)-[:SON_OF]->(SunandaI)


CREATE (Sushraba:Person {name:'Sushraba', gender: 'Female'})
CREATE (Arbachin:Person {name:'Arbachin', gender: 'Male'})
CREATE
(Jayatsen)-[:HUSBAND_OF]->(Sushraba),
(Sushraba)-[:WIFE_OF]->(Jayatsen),
(Jayatsen)-[:FATHER_OF]->(Arbachin),
(Sushraba)-[:MOTHER_OF]->(Arbachin),
(Arbachin)-[:SON_OF]->(Jayatsen),
(Arbachin)-[:SON_OF]->(Sushraba)


CREATE (MaryadaI:Person {name:'Maryada (I)', gender: 'Female'})
CREATE (ArihanI:Person {name:'Arihan (I)', gender: 'Male'})
CREATE
(Arbachin)-[:HUSBAND_OF]->(MaryadaI),
(MaryadaI)-[:WIFE_OF]->(Arbachin),
(Arbachin)-[:FATHER_OF]->(ArihanI),
(MaryadaI)-[:MOTHER_OF]->(ArihanI),
(ArihanI)-[:SON_OF]->(Arbachin),
(ArihanI)-[:SON_OF]->(MaryadaI)


CREATE (Angi:Person {name:'Angi', gender: 'Female'})
CREATE (Mahabhauma:Person {name:'Mahabhauma', gender: 'Male'})
CREATE
(ArihanI)-[:HUSBAND_OF]->(Angi),
(Angi)-[:WIFE_OF]->(ArihanI),
(ArihanI)-[:FATHER_OF]->(Mahabhauma),
(Angi)-[:MOTHER_OF]->(Mahabhauma),
(Mahabhauma)-[:SON_OF]->(ArihanI),
(Mahabhauma)-[:SON_OF]->(Angi)

CREATE (Suyajna:Person {name:'Suyajna', gender: 'Female'})
CREATE (Ayutanayin:Person {name:'Ayutanayin', gender: 'Male'})
CREATE
(Mahabhauma)-[:HUSBAND_OF]->(Suyajna),
(Suyajna)-[:WIFE_OF]->(Mahabhauma),
(Mahabhauma)-[:FATHER_OF]->(Ayutanayin),
(Suyajna)-[:MOTHER_OF]->(Ayutanayin),
(Ayutanayin)-[:SON_OF]->(Mahabhauma),
(Ayutanayin)-[:SON_OF]->(Suyajna)


CREATE (Kama:Person {name:'Kama', gender: 'Female'})
CREATE (Akrodhana:Person {name:'Akrodhana', gender: 'Male'})
CREATE
(Ayutanayin)-[:HUSBAND_OF]->(Kama),
(Kama)-[:WIFE_OF]->(Ayutanayin),
(Ayutanayin)-[:FATHER_OF]->(Akrodhana),
(Kama)-[:MOTHER_OF]->(Akrodhana),
(Akrodhana)-[:SON_OF]->(Ayutanayin),
(Akrodhana)-[:SON_OF]->(Kama)

CREATE (Karambha:Person {name:'Karambha', gender: 'Female'})
CREATE (Devatithi:Person {name:'Devatithi', gender: 'Male'})
CREATE
(Akrodhana)-[:HUSBAND_OF]->(Karambha),
(Karambha)-[:WIFE_OF]->(Akrodhana),
(Akrodhana)-[:FATHER_OF]->(Devatithi),
(Karambha)-[:MOTHER_OF]->(Devatithi),
(Devatithi)-[:SON_OF]->(Akrodhana),
(Devatithi)-[:SON_OF]->(Karambha)

CREATE (MaryadaII:Person {name:'Maryada (II)', gender: 'Female'})
CREATE (ArihanII:Person {name:'Arihan (II)', gender: 'Male'})
CREATE
(Devatithi)-[:HUSBAND_OF]->(MaryadaII),
(MaryadaII)-[:WIFE_OF]->(Devatithi),
(Devatithi)-[:FATHER_OF]->(ArihanII),
(MaryadaII)-[:MOTHER_OF]->(ArihanII),
(ArihanII)-[:SON_OF]->(Devatithi),
(ArihanII)-[:SON_OF]->(MaryadaII)


CREATE (SudevaI:Person {name:'Sudeva (I)', gender: 'Female'})
CREATE (Rksha:Person {name:'Rksha', gender: 'Male'})
CREATE
(ArihanII)-[:HUSBAND_OF]->(SudevaI),
(SudevaI)-[:WIFE_OF]->(ArihanII),
(ArihanII)-[:FATHER_OF]->(Rksha),
(SudevaI)-[:MOTHER_OF]->(Rksha),
(Rksha)-[:SON_OF]->(ArihanII),
(Rksha)-[:SON_OF]->(SudevaI)


CREATE (Jwala:Person {name:'Jwala', gender: 'Female'})
CREATE (Motinara:Person {name:'Motinara', gender: 'Male'})
CREATE
(Rksha)-[:HUSBAND_OF]->(Jwala),
(Jwala)-[:WIFE_OF]->(Rksha),
(Rksha)-[:FATHER_OF]->(Motinara),
(Jwala)-[:MOTHER_OF]->(Motinara),
(Motinara)-[:SON_OF]->(Rksha),
(Motinara)-[:SON_OF]->(Jwala)


CREATE (Saraswati:Person {name:'Saraswati (Manasvini)', gender: 'Female'})
CREATE (Tansu:Person {name:'Tansu', gender: 'Male'})
CREATE
(Motinara)-[:HUSBAND_OF]->(Saraswati),
(Saraswati)-[:WIFE_OF]->(Motinara),
(Motinara)-[:FATHER_OF]->(Tansu),
(Saraswati)-[:MOTHER_OF]->(Tansu),
(Tansu)-[:SON_OF]->(Motinara),
(Tansu)-[:SON_OF]->(Saraswati)

CREATE (Kalindi:Person {name:'Kalindi', gender: 'Female'})
CREATE (Ilina:Person {name:'Ilina', gender: 'Male'})
CREATE
(Tansu)-[:HUSBAND_OF]->(Kalindi),
(Kalindi)-[:WIFE_OF]->(Tansu),
(Tansu)-[:FATHER_OF]->(Ilina),
(Kalindi)-[:MOTHER_OF]->(Ilina),
(Ilina)-[:SON_OF]->(Tansu),
(Ilina)-[:SON_OF]->(Kalindi)


CREATE (Rathantari:Person {name:'Rathantari', gender: 'Female'})
CREATE (Dushyanta:Person {name:'Dushyanta', gender: 'Male', title: 'King'})
CREATE
(Ilina)-[:HUSBAND_OF]->(Rathantari),
(Rathantari)-[:WIFE_OF]->(Ilina),
(Ilina)-[:FATHER_OF]->(Dushyanta),
(Rathantari)-[:MOTHER_OF]->(Dushyanta),
(Dushyanta)-[:SON_OF]->(Ilina),
(Dushyanta)-[:SON_OF]->(Rathantari)


CREATE (Shakuntala:Person {name:'Shakuntala', gender: 'Female'})
CREATE (Bharata:Person {name:'Bharata', gender: 'Male', title: 'King'})
CREATE
(Dushyanta)-[:HUSBAND_OF]->(Shakuntala),
(Shakuntala)-[:WIFE_OF]->(Dushyanta),
(Dushyanta)-[:FATHER_OF]->(Bharata),
(Shakuntala)-[:MOTHER_OF]->(Bharata),
(Bharata)-[:SON_OF]->(Dushyanta),
(Bharata)-[:SON_OF]->(Shakuntala)


CREATE (SunandaII:Person {name:'Sunanda (II)', gender: 'Female'})
CREATE (Bhumanyu:Person {name:'Bhumanyu', gender: 'Male', title: 'Prince'})
CREATE
(Bharata)-[:HUSBAND_OF]->(SunandaII),
(SunandaII)-[:WIFE_OF]->(Bharata),
(Bharata)-[:FATHER_OF]->(Bhumanyu),
(SunandaII)-[:MOTHER_OF]->(Bhumanyu),
(Bhumanyu)-[:SON_OF]->(Bharata),
(Bhumanyu)-[:SON_OF]->(SunandaII)


CREATE (Vijaya:Person {name:'Vijaya', gender: 'Female'})
CREATE (Suhotra:Person {name:'Suhotra', gender: 'Male'})
CREATE
(Bhumanyu)-[:HUSBAND_OF]->(Vijaya),
(Vijaya)-[:WIFE_OF]->(Bhumanyu),
(Bhumanyu)-[:FATHER_OF]->(Suhotra),
(Vijaya)-[:MOTHER_OF]->(Suhotra),
(Suhotra)-[:SON_OF]->(Bhumanyu),
(Suhotra)-[:SON_OF]->(Vijaya)


CREATE (Suvarna:Person {name:'Suvarna', gender: 'Female'})
CREATE (Hasti:Person {name:'Hasti', gender: 'Male', title: 'King'})
CREATE
(Suhotra)-[:HUSBAND_OF]->(Suvarna),
(Suvarna)-[:WIFE_OF]->(Suhotra),
(Suhotra)-[:FATHER_OF]->(Hasti),
(Suvarna)-[:MOTHER_OF]->(Hasti),
(Hasti)-[:SON_OF]->(Suhotra),
(Hasti)-[:SON_OF]->(Suvarna)


CREATE (Yashodhara:Person {name:'Yashodhara', gender: 'Female'})
CREATE (Vikunthana:Person {name:'Vikunthana', gender: 'Male', title: 'King'})
CREATE
(Hasti)-[:HUSBAND_OF]->(Yashodhara),
(Yashodhara)-[:WIFE_OF]->(Hasti),
(Hasti)-[:FATHER_OF]->(Vikunthana),
(Yashodhara)-[:MOTHER_OF]->(Vikunthana),
(Vikunthana)-[:SON_OF]->(Hasti),
(Vikunthana)-[:SON_OF]->(Yashodhara)


CREATE (SudevaII:Person {name:'Sudeva (II)', gender: 'Female'})
CREATE (Ajmeed:Person {name:'Ajmeed', gender: 'Male'})
CREATE
(Vikunthana)-[:HUSBAND_OF]->(SudevaII),
(SudevaII)-[:WIFE_OF]->(Vikunthana),
(Vikunthana)-[:FATHER_OF]->(Ajmeed),
(SudevaII)-[:MOTHER_OF]->(Ajmeed),
(Ajmeed)-[:SON_OF]->(Vikunthana),
(Ajmeed)-[:SON_OF]->(SudevaII)

CREATE (Kaikeyi:Person {name:'Kaikeyi', gender: 'Female'})
CREATE (Samvarana:Person {name:'Samvarana', gender: 'Male', title: 'King'})
CREATE
(Ajmeed)-[:HUSBAND_OF]->(Kaikeyi),
(Kaikeyi)-[:WIFE_OF]->(Ajmeed),
(Ajmeed)-[:FATHER_OF]->(Samvarana),
(Kaikeyi)-[:MOTHER_OF]->(Samvarana),
(Samvarana)-[:SON_OF]->(Ajmeed),
(Samvarana)-[:SON_OF]->(Kaikeyi)


CREATE (Tapati:Person {name:'Tapati', gender: 'Female'})
CREATE (Kuru:Person {name:'Kuru', gender: 'Male', title: 'King'})
CREATE
(Samvarana)-[:HUSBAND_OF]->(Tapati),
(Tapati)-[:WIFE_OF]->(Samvarana),
(Samvarana)-[:FATHER_OF]->(Kuru),
(Tapati)-[:MOTHER_OF]->(Kuru),
(Kuru)-[:SON_OF]->(Samvarana),
(Kuru)-[:SON_OF]->(Tapati)


CREATE (Subhangi:Person {name:'Subhangi', gender: 'Female'})
CREATE (Viduratha:Person {name:'Viduratha', gender: 'Male', title: 'King'})
CREATE
(Kuru)-[:HUSBAND_OF]->(Subhangi),
(Subhangi)-[:WIFE_OF]->(Kuru),
(Kuru)-[:FATHER_OF]->(Viduratha),
(Subhangi)-[:MOTHER_OF]->(Viduratha),
(Viduratha)-[:SON_OF]->(Kuru),
(Viduratha)-[:SON_OF]->(Subhangi)


CREATE (Sampriya:Person {name:'Sampriya', gender: 'Female'})
CREATE (Anaswan:Person {name:'Anaswan', gender: 'Male', title: 'King'})
CREATE
(Viduratha)-[:HUSBAND_OF]->(Sampriya),
(Sampriya)-[:WIFE_OF]->(Viduratha),
(Viduratha)-[:FATHER_OF]->(Anaswan),
(Sampriya)-[:MOTHER_OF]->(Anaswan),
(Anaswan)-[:SON_OF]->(Viduratha),
(Anaswan)-[:SON_OF]->(Sampriya)


CREATE (Amrita:Person {name:'Amrita', gender: 'Female'})
CREATE (ParikshitaI:Person {name:'Parikshita (I)', gender: 'Male', title: 'King'})
CREATE
(Anaswan)-[:HUSBAND_OF]->(Amrita),
(Amrita)-[:WIFE_OF]->(Anaswan),
(Anaswan)-[:FATHER_OF]->(ParikshitaI),
(Amrita)-[:MOTHER_OF]->(ParikshitaI),
(ParikshitaI)-[:SON_OF]->(Anaswan),
(ParikshitaI)-[:SON_OF]->(Amrita)


CREATE (Suyasha:Person {name:'Suyasha', gender: 'Female'})
CREATE (BheemsenaI:Person {name:'Bheemsena (I)', gender: 'Male', title: 'King'})
CREATE
(ParikshitaI)-[:HUSBAND_OF]->(Suyasha),
(Suyasha)-[:WIFE_OF]->(ParikshitaI),
(ParikshitaI)-[:FATHER_OF]->(BheemsenaI),
(Suyasha)-[:MOTHER_OF]->(BheemsenaI),
(BheemsenaI)-[:SON_OF]->(ParikshitaI),
(BheemsenaI)-[:SON_OF]->(Suyasha)


CREATE (Kumari:Person {name:'Kumari', gender: 'Female'})
CREATE (Pratishrava:Person {name:'Pratishrava', gender: 'Male', title: 'Prince'})
CREATE
(BheemsenaI)-[:HUSBAND_OF]->(Kumari),
(Kumari)-[:WIFE_OF]->(BheemsenaI),
(BheemsenaI)-[:FATHER_OF]->(Pratishrava),
(Kumari)-[:MOTHER_OF]->(Pratishrava),
(Pratishrava)-[:SON_OF]->(BheemsenaI),
(Pratishrava)-[:SON_OF]->(Kumari)


CREATE (Pratipa:Person {name:'Pratipa', gender: 'Male', title: 'King'})
CREATE (Pratishrava)-[:FATHER_OF]->(Pratipa)


CREATE (SunandaIII:Person {name:'Sunanda (III)', gender: 'Female'})
CREATE (Shantanu:Person {name:'Shantanu', gender: 'Male', title: 'King'})
CREATE
(Pratipa)-[:HUSBAND_OF]->(SunandaIII),
(SunandaIII)-[:WIFE_OF]->(Pratipa),
(Pratipa)-[:FATHER_OF]->(Shantanu),
(SunandaIII)-[:MOTHER_OF]->(Shantanu),
(Shantanu)-[:SON_OF]->(Pratipa),
(Shantanu)-[:SON_OF]->(SunandaIII)


CREATE (Ganga:Person {name:'Ganga', gender: 'Female'})
CREATE (Bhishma:Person {name:'Bhishma', gender: 'Male', title: 'Prince', nickname: 'Devavrata', marital_status: 'Unmarried'})
CREATE (Chitrangada:Person {name:'Chitrangada', gender: 'Male', title: 'Prince', marital_status: 'Unmarried'})
CREATE (Vichitravirya:Person {name:'Vichitravirya', gender: 'Male', title: 'King', marital_status: 'Married'})
CREATE (Satyavati:Person {name:'Satyavati', gender: 'Female'})
CREATE (KrishnaDweepayanaVedVyasa:Person {name:'Krishna Dweepayana Ved Vyasa', gender: 'Male'})
CREATE (Parashara:Person {name:'Parashara', gender: 'Male', title: 'Sage'})
CREATE
(Shantanu)-[:HUSBAND_OF]->(Ganga),
(Ganga)-[:WIFE_OF]->(Shantanu),
(Shantanu)-[:FATHER_OF]->(Bhishma),
(Ganga)-[:MOTHER_OF]->(Bhishma),
(Bhishma)-[:SON_OF]->(Shantanu),
(Bhishma)-[:SON_OF]->(Ganga),

(Shantanu)-[:HUSBAND_OF]->(Satyavati),
(Satyavati)-[:WIFE_OF]->(Shantanu),
(Shantanu)-[:FATHER_OF]->(Chitrangada),
(Satyavati)-[:MOTHER_OF]->(Chitrangada),
(Chitrangada)-[:SON_OF]->(Shantanu),
(Chitrangada)-[:SON_OF]->(Satyavati),
(Shantanu)-[:FATHER_OF]->(Vichitravirya),
(Satyavati)-[:MOTHER_OF]->(Vichitravirya),
(Vichitravirya)-[:SON_OF]->(Shantanu),
(Vichitravirya)-[:SON_OF]->(Satyavati),

(Parashara)-[:FATHER_OF]->(KrishnaDweepayanaVedVyasa),
(Satyavati)-[:MOTHER_OF]->(KrishnaDweepayanaVedVyasa),
(KrishnaDweepayanaVedVyasa)-[:SON_OF]->(Parashara),
(KrishnaDweepayanaVedVyasa)-[:SON_OF]->(Satyavati)


CREATE (Ambika:Person {name:'Ambika', gender: 'Female'})
CREATE (Ambalika:Person {name:'Ambalika', gender: 'Female'})
CREATE
(Vichitravirya)-[:HUSBAND_OF]->(Ambika),
(Vichitravirya)-[:HUSBAND_OF]->(Ambalika),
(Ambika)-[:WIFE_OF]->(Vichitravirya),
(Ambalika)-[:WIFE_OF]->(Vichitravirya)


CREATE (Dhritarashtra:Person {name:'Dhritarashtra', gender: 'Male', title: 'King', health: 'Blind'})
CREATE (Pandu:Person {name:'Pandu', gender: 'Male', title: 'King'})
CREATE (Vidura:Person {name:'Vidura', gender: 'Male', title: 'Prince'})
CREATE
(KrishnaDweepayanaVedVyasa)-[:FATHER_OF]->(Dhritarashtra),
(KrishnaDweepayanaVedVyasa)-[:FATHER_OF]->(Pandu),
(KrishnaDweepayanaVedVyasa)-[:FATHER_OF]->(Vidura),
(Ambika)-[:MOTHER_OF]->(Dhritarashtra),
(Ambalika)-[:MOTHER_OF]->(Pandu)


CREATE (Gandhari:Person {name:'Gandhari', gender: 'Female'})
CREATE (Dushala:Person {name:'Dushala', gender: 'Female'})
CREATE (Yuyutsu:Person {name:'Yuyutsu', gender: 'Male', title: 'Prince'})
CREATE (Jayadratha:Person {name:'Jayadratha', gender: 'Male', title: 'Prince'})
CREATE (Duryodhana:Person {name:'Duryodhana', gender: 'Male', title: 'Prince', type: 'Kauravas'})
CREATE (LaxmanaKumar:Person {name:'Laxmana Kumar', gender: 'Male', title: 'Prince'})
CREATE (Kaalketu:Person {name:'Kaalketu', gender: 'Male', title: 'Prince'})
CREATE (Laxamanaa:Person {name:'Laxamanaa', gender: 'Female'})
CREATE (Dushasana:Person {name:'Dushasana', gender: 'Male', title: 'Prince', type: 'Kauravas'})
CREATE (Durmashana:Person {name:'Durmashana', gender: 'Male', title: 'Prince'})
CREATE
(Dhritarashtra)-[:HUSBAND_OF]->(Gandhari),
(Gandhari)-[:WIFE_OF]->(Dhritarashtra),
(Gandhari)-[:MOTHER_OF {number_of_children: 101}]->(Duryodhana),
(Gandhari)-[:MOTHER_OF {number_of_children: 101}]->(Dushasana),
(Gandhari)-[:MOTHER_OF]->(Dushala),
(Dhritarashtra)-[:FATHER_OF]->(Yuyutsu),
(Yuyutsu)-[:SON_OF]->(Dhritarashtra),
(Jayadratha)-[:HUSBAND_OF]->(Dushala),
(Dushala)-[:WIFE_OF]->(Jayadratha),
(Duryodhana)-[:HUSBAND_OF]->(Bhanumati),
(Bhanumati)-[:WIFE_OF]->(Duryodhana),
(Dhritarashtra)-[:FATHER_OF]->(Duryodhana),
(Dhritarashtra)-[:FATHER_OF]->(Dushasana),
(Dhritarashtra)-[:FATHER_OF]->(Dushala),
(Gandhari)-[:MOTHER_OF]->(Duryodhana),
(Gandhari)-[:MOTHER_OF]->(Dushasana),
(Gandhari)-[:MOTHER_OF]->(Dushala),
(Duryodhana)-[:SON_OF]->(Dhritarashtra),
(Dushasana)-[:SON_OF]->(Dhritarashtra),
(Dushala)-[:DAUGHTER_OF]->(Dhritarashtra),
(Duryodhana)-[:SON_OF]->(Gandhari),
(Dushasana)-[:SON_OF]->(Gandhari),
(Dushala)-[:DAUGHTER_OF]->(Gandhari),
(Duryodhana)-[:FATHER_OF]->(LaxmanaKumar),
(Duryodhana)-[:FATHER_OF]->(Kaalketu),
(Duryodhana)-[:FATHER_OF]->(Laxamanaa),
(LaxmanaKumar)-[:SON_OF]->(Duryodhana),
(Kaalketu)-[:SON_OF]->(Duryodhana),
(Laxamanaa)-[:DAUGHTER_OF]->(Duryodhana),
(Dushasana)-[:FATHER_OF]->(Durmashana),
(Durmashana)-[:SON_OF]->(Dushasana)


CREATE (Kunti:Person {name:'Kunti', gender: 'Female'})
CREATE (Madri:Person {name:'Madri', gender: 'Female'})
CREATE (Yudhishthira:Person {name:'Yudhishthira', gender: 'Male', title: 'Prince'})
CREATE (Bheema:Person {name:'Bheema', gender: 'Male', title: 'Prince'})
CREATE (Arjuna:Person {name:'Arjuna', gender: 'Male', title: 'Prince'})
CREATE (Karna:Person {name:'Karna', gender: 'Male', title: 'Prince'})
CREATE (Nakula:Person {name:'Nakula', gender: 'Male', title: 'Prince'})
CREATE (Sahadeva:Person {name:'Sahadeva', gender: 'Male', title: 'Prince'})
CREATE (Yamraj:Person {name:'Yamraj', gender: 'Male', title: 'Lord'})
CREATE (Vayudeva:Person {name:'Vayudeva', gender: 'Male', title: 'Lord'})
CREATE (Indra:Person {name:'Indra', gender: 'Male', title: 'Lord'})
CREATE (LordSurya:Person {name:'Lord Surya', gender: 'Male', title: 'Lord'})
CREATE (AshviniKumaras:Person {name:'Ashvini Kumaras', gender: 'Male', title: 'Lord'})
CREATE
(Pandu)-[:HUSBAND_OF]->(Kunti),
(Pandu)-[:HUSBAND_OF]->(Madri),
(Kunti)-[:WIFE_OF]->(Pandu),
(Madri)-[:WIFE_OF]->(Pandu),
(Yamraj)-[:FATHER_OF]->(Yudhishthira),
(Kunti)-[:MOTHER_OF]->(Yudhishthira),
(Yudhishthira)-[:SON_OF]->(Yamraj),
(Yudhishthira)-[:SON_OF]->(Kunti),
(Vayudeva)-[:FATHER_OF]->(Bheema),
(Kunti)-[:MOTHER_OF]->(Bheema),
(Bheema)-[:SON_OF]->(Vayudeva),
(Bheema)-[:SON_OF]->(Kunti),
(Indra)-[:FATHER_OF]->(Arjuna),
(Kunti)-[:MOTHER_OF]->(Arjuna),
(Arjuna)-[:SON_OF]->(Indra),
(Arjuna)-[:SON_OF]->(Kunti),
(LordSurya)-[:FATHER_OF]->(Karna),
(Kunti)-[:MOTHER_OF]->(Karna),
(Karna)-[:SON_OF]->(LordSurya),
(Karna)-[:SON_OF]->(Kunti),
(AshviniKumaras)-[:FATHER_OF]->(Nakula),
(Madri)-[:MOTHER_OF]->(Nakula),
(Nakula)-[:SON_OF]->(AshviniKumaras),
(Nakula)-[:SON_OF]->(Madri),
(AshviniKumaras)-[:FATHER_OF]->(Sahadeva),
(Madri)-[:MOTHER_OF]->(Sahadeva),
(Sahadeva)-[:SON_OF]->(AshviniKumaras),
(Sahadeva)-[:SON_OF]->(Madri)


CREATE (Vrushali:Person {name:'Vrushali', gender: 'Female'})
CREATE (Supriya:Person {name:'Supriya', gender: 'Female'})

CREATE (Shatrunjaya:Person {name:'Shatrunjaya', gender: 'Male', title: 'Prince'})
CREATE (Vrishasena:Person {name:'Vrishasena', gender: 'Male', title: 'Prince'})
CREATE (Dvipada:Person {name:'Dvipada', gender: 'Male', title: 'Prince'})
CREATE (Sushena:Person {name:'Sushena', gender: 'Male', title: 'Prince'})
CREATE (Chitrasena:Person {name:'Chitrasena', gender: 'Male', title: 'Prince'})
CREATE (Satyasena:Person {name:'Satyasena', gender: 'Male', title: 'Prince'})
CREATE (Susharma:Person {name:'Susharma', gender: 'Male', title: 'Prince'})
CREATE (Vrishaketu:Person {name:'Vrishaketu', gender: 'Male', title: 'Prince'})
CREATE (Sudharma:Person {name:'Sudharma', gender: 'Male', title: 'Prince'})
CREATE
(Karna)-[:HUSBAND_OF]->(Vrushali),
(Karna)-[:HUSBAND_OF]->(Supriya),
(Vrushali)-[:WIFE_OF]->(Karna),
(Supriya)-[:WIFE_OF]->(Karna),
(Karna)-[:FATHER_OF]->(Shatrunjaya),
(Karna)-[:FATHER_OF]->(Vrishasena),
(Karna)-[:FATHER_OF]->(Dvipada),
(Karna)-[:FATHER_OF]->(Sushena),
(Karna)-[:FATHER_OF]->(Chitrasena),
(Karna)-[:FATHER_OF]->(Satyasena),
(Karna)-[:FATHER_OF]->(Susharma),
(Karna)-[:FATHER_OF]->(Vrishaketu),
(Karna)-[:FATHER_OF]->(Sudharma),
(Arjuna)-[:KILLED]->(Shatrunjaya),
(Arjuna)-[:KILLED]->(Vrishasena),
(Arjuna)-[:KILLED]->(Dvipada),
(Yudhishthira)-[:KILLED]->(Sushena),
(Nakula)-[:KILLED]->(Chitrasena),
(Nakula)-[:KILLED]->(Satyasena),
(Nakula)-[:KILLED]->(Susharma)


CREATE (Draupadi:Person {name:'Draupadi', gender: 'Female'})
CREATE (Devika:Person {name:'Devika', gender: 'Female'})
CREATE (Yaudheya:Person {name:'Yaudheya', gender: 'Male', title: 'Prince'})
CREATE (Prativindya:Person {name:'Prativindya', gender: 'Male', title: 'Prince'})
CREATE
(Yudhishthira)-[:HUSBAND_OF]->(Draupadi),
(Yudhishthira)-[:HUSBAND_OF]->(Devika),
(Draupadi)-[:WIFE_OF]->(Yudhishthira),
(Devika)-[:WIFE_OF]->(Yudhishthira),
(Yudhishthira)-[:FATHER_OF]->(Yaudheya),
(Devika)-[:MOTHER_OF]->(Yaudheya),
(Yaudheya)-[:SON_OF]->(Yudhishthira),
(Yaudheya)-[:SON_OF]->(Devika),
(Yudhishthira)-[:FATHER_OF]->(Prativindya),
(Draupadi)-[:MOTHER_OF]->(Prativindya),
(Prativindya)-[:SON_OF]->(Yudhishthira),
(Prativindya)-[:SON_OF]->(Draupadi)


CREATE (Karenumti:Person {name:'Karenumti', gender: 'Female'})
CREATE (Satanika:Person {name:'Satanika', gender: 'Male', title: 'Prince'})
CREATE (Niramitra:Person {name:'Niramitra', gender: 'Male', title: 'Prince'})
CREATE
(Nakula)-[:HUSBAND_OF]->(Karenumti),
(Nakula)-[:HUSBAND_OF]->(Draupadi),
(Karenumti)-[:WIFE_OF]->(Nakula),
(Draupadi)-[:WIFE_OF]->(Nakula),
(Nakula)-[:FATHER_OF]->(Satanika),
(Draupadi)-[:MOTHER_OF]->(Satanika),
(Satanika)-[:SON_OF]->(Nakula),
(Satanika)-[:SON_OF]->(Draupadi),
(Nakula)-[:FATHER_OF]->(Niramitra),
(Karenumti)-[:MOTHER_OF]->(Niramitra),
(Niramitra)-[:SON_OF]->(Nakula),
(Niramitra)-[:SON_OF]->(Karenumti)

CREATE (Shrutasena:Person {name:'Shrutasena', gender: 'Male', title: 'Prince'})
CREATE
(Sahadeva)-[:HUSBAND_OF]->(Vijaya),
(Sahadeva)-[:HUSBAND_OF]->(Draupadi),
(Vijaya)-[:WIFE_OF]->(Sahadeva),
(Draupadi)-[:WIFE_OF]->(Sahadeva),
(Sahadeva)-[:FATHER_OF]->(Shrutasena),
(Draupadi)-[:MOTHER_OF]->(Shrutasena),
(Shrutasena)-[:SON_OF]->(Sahadeva),
(Shrutasena)-[:SON_OF]->(Draupadi),
(Sahadeva)-[:FATHER_OF]->(Suhotra),
(Vijaya)-[:MOTHER_OF]->(Suhotra),
(Suhotra)-[:SON_OF]->(Sahadeva),
(Suhotra)-[:SON_OF]->(Vijaya)


CREATE (Hidimba:Person {name:'Hidimba', gender: 'Female'})
CREATE (Valandhara:Person {name:'Valandhara', gender: 'Female'})
CREATE (Ghatotakach:Person {name:'Ghatotakach', gender: 'Male', title: 'Prince'})
CREATE (Sutasoma:Person {name:'Sutasoma', gender: 'Male', title: 'Prince'})
CREATE (Sarvaga:Person {name:'Sarvaga', gender: 'Male', title: 'Prince'})
CREATE
(Bheema)-[:HUSBAND_OF]->(Hidimba),
(Bheema)-[:HUSBAND_OF]->(Draupadi),
(Bheema)-[:HUSBAND_OF]->(Valandhara),
(Hidimba)-[:WIFE_OF]->(Bheema),
(Valandhara)-[:WIFE_OF]->(Bheema),
(Draupadi)-[:WIFE_OF]->(Bheema),
(Bheema)-[:FATHER_OF]->(Ghatotakach),
(Hidimba)-[:MOTHER_OF]->(Ghatotakach),
(Ghatotakach)-[:SON_OF]->(Bheema),
(Ghatotakach)-[:SON_OF]->(Hidimba),
(Bheema)-[:FATHER_OF]->(Sutasoma),
(Draupadi)-[:MOTHER_OF]->(Sutasoma),
(Sutasoma)-[:SON_OF]->(Bheema),
(Sutasoma)-[:SON_OF]->(Draupadi),
(Bheema)-[:FATHER_OF]->(Sarvaga),
(Valandhara)-[:MOTHER_OF]->(Sarvaga),
(Sarvaga)-[:SON_OF]->(Bheema),
(Sarvaga)-[:SON_OF]->(Valandhara)


CREATE (Chitangada:Person {name:'Chitangada', gender: 'Female'})
CREATE (Ulupi:Person {name:'Ulupi', gender: 'Female'})
CREATE (Subhadra:Person {name:'Subhadra', gender: 'Female'})
CREATE (Shrutakarma:Person {name:'Shrutakarma', gender: 'Male', title: 'Prince'})
CREATE (Abhimanyu:Person {name:'Abhimanyu', gender: 'Male', title: 'Prince'})
CREATE (Iravan:Person {name:'Iravan', gender: 'Male', title: 'Prince'})
CREATE (Babruvahana:Person {name:'Babruvahana', gender: 'Male', title: 'Prince'})
CREATE
(Arjuna)-[:HUSBAND_OF]->(Draupadi),
(Arjuna)-[:HUSBAND_OF]->(Chitangada),
(Arjuna)-[:HUSBAND_OF]->(Ulupi),
(Arjuna)-[:HUSBAND_OF]->(Subhadra),
(Draupadi)-[:WIFE_OF]->(Arjuna),
(Chitangada)-[:WIFE_OF]->(Arjuna),
(Ulupi)-[:WIFE_OF]->(Arjuna),
(Subhadra)-[:WIFE_OF]->(Arjuna),
(Arjuna)-[:FATHER_OF]->(Shrutakarma),
(Arjuna)-[:FATHER_OF]->(Abhimanyu),
(Arjuna)-[:FATHER_OF]->(Iravan),
(Arjuna)-[:FATHER_OF]->(Babruvahana),
(Draupadi)-[:MOTHER_OF]->(Shrutakarma),
(Subhadra)-[:MOTHER_OF]->(Abhimanyu),
(Ulupi)-[:MOTHER_OF]->(Iravan),
(Chitangada)-[:MOTHER_OF]->(Babruvahana),
(Shrutakarma)-[:SON_OF]->(Arjuna),
(Abhimanyu)-[:SON_OF]->(Arjuna),
(Iravan)-[:SON_OF]->(Arjuna),
(Babruvahana)-[:SON_OF]->(Arjuna),
(Shrutakarma)-[:SON_OF]->(Draupadi),
(Abhimanyu)-[:SON_OF]->(Subhadra),
(Iravan)-[:SON_OF]->(Ulupi),
(Babruvahana)-[:SON_OF]->(Chitangada),
(Babruvahana)-[:KILLED]->(Vrishaketu)


CREATE (Uttara:Person {name:'Uttara', gender: 'Female'})
CREATE (ParikshitII:Person {name:'Parikshit (II)', gender: 'Male', title: 'King'})
CREATE
(Abhimanyu)-[:HUSBAND_OF]->(Uttara),
(Uttara)-[:WIFE_OF]->(Abhimanyu),
(Abhimanyu)-[:FATHER_OF]->(ParikshitII),
(Uttara)-[:MOTHER_OF]->(ParikshitII),
(ParikshitII)-[:SON_OF]->(Uttara),
(ParikshitII)-[:SON_OF]->(Abhimanyu)


CREATE (Madravati:Person {name:'Madravati', gender: 'Female'})
CREATE (JanmejayaII:Person {name:'Janmejaya (II)', gender: 'Male', title: 'King'})
CREATE
(ParikshitII)-[:HUSBAND_OF]->(Madravati),
(Madravati)-[:WIFE_OF]->(ParikshitII),
(ParikshitII)-[:FATHER_OF]->(JanmejayaII),
(Madravati)-[:MOTHER_OF]->(JanmejayaII),
(JanmejayaII)-[:SON_OF]->(ParikshitII),
(JanmejayaII)-[:SON_OF]->(Madravati)


CREATE (Bapusthama:Person {name:'Bapusthama', gender: 'Female'})
CREATE (ShatanikII:Person {name:'Shatanik (II)', gender: 'Male', title: 'King'})
CREATE
(JanmejayaII)-[:HUSBAND_OF]->(Bapusthama),
(Bapusthama)-[:WIFE_OF]->(JanmejayaII),
(JanmejayaII)-[:FATHER_OF]->(ShatanikII),
(Bapusthama)-[:MOTHER_OF]->(ShatanikII),
(ShatanikII)-[:SON_OF]->(Bapusthama),
(ShatanikII)-[:SON_OF]->(JanmejayaII)


CREATE (Baidehi:Person {name:'Baidehi', gender: 'Female'})
CREATE (Ashvamedhadutta:Person {name:'Ashvamedhadutta', gender: 'Male', title: 'Prince'})
CREATE
(ShatanikII)-[:HUSBAND_OF]->(Baidehi),
(Baidehi)-[:WIFE_OF]->(ShatanikII),
(ShatanikII)-[:FATHER_OF]->(Ashvamedhadutta),
(Baidehi)-[:MOTHER_OF]->(Ashvamedhadutta),
(Ashvamedhadutta)-[:SON_OF]->(ShatanikII),
(Ashvamedhadutta)-[:SON_OF]->(Baidehi),
(Karna)-[:KILLED]->(Ghatotakach)
