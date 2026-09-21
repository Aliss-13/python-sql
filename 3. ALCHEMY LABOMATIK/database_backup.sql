BEGIN TRANSACTION;
CREATE TABLE affinities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    , icon TEXT);
INSERT INTO "affinities" VALUES(1,'Lumière','⚪');
INSERT INTO "affinities" VALUES(2,'Ombre','🟣');
INSERT INTO "affinities" VALUES(3,'Feu','🔥');
INSERT INTO "affinities" VALUES(4,'Eau','💧');
INSERT INTO "affinities" VALUES(5,'Vent','🌪️');
INSERT INTO "affinities" VALUES(6,'Plante','🌱');
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    rarity_id INTEGER, description TEXT, category_id INTEGER,
    FOREIGN KEY (rarity_id) REFERENCES rarities(id)
);
INSERT INTO "equipment" VALUES(1,'Pilon rudimentaire',1,'Pratique pour écraser des trucs.',1);
INSERT INTO "equipment" VALUES(2,'Chaudron de cuivre',1,'Pour faire les soupes et les permanentes.',2);
INSERT INTO "equipment" VALUES(3,'Feu classique',1,'Le feu, ça brûle.',3);
INSERT INTO "equipment" VALUES(4,'Fiole en verre',1,'Comme ça, on en met pas de partout dans sa besace.',4);
INSERT INTO "equipment" VALUES(5,'Fiole piriforme',2,'Un joli contenant en forme de poire.',4);
INSERT INTO "equipment" VALUES(6,'Mortier d''alchimiste',1,'Un mélangeur semi-professionnel.',1);
INSERT INTO "equipment" VALUES(7,'Mixeur arcanique',2,'Destructure l''intemporalité grâce à la technologie Brushless® de ses lames rotatives.',1);
INSERT INTO "equipment" VALUES(8,'Moulingex Baby Cook®',3,'Indispensable pour tout alchimiste qui se respecte. Prépare aussi facilement et rapidement les repas de Bébé.',1);
INSERT INTO "equipment" VALUES(9,'Thermomix 9000 DolbyTHX',4,'Le mixeur testostéroné qui fait pas dans la dentelle. Si vous pouvez tacher moyen de vous éloigner de vingt-cinq pieds, bon pieds hein parce que ça va gicler un peu.',1);
INSERT INTO "equipment" VALUES(10,'Gazinière cryogénique',2,'Frissons garantis !',3);
INSERT INTO "equipment" VALUES(11,'Générateur de courant alternatif',2,'Bien charger en plutonium avant utilisation.',3);
INSERT INTO "equipment" VALUES(12,'Mini trou noir portatif',3,'Ne pas avaler.',3);
INSERT INTO "equipment" VALUES(13,'Tornade naine',3,'Mieux connue simplement sous le nom de Taz.',3);
INSERT INTO "equipment" VALUES(14,'Tcherno-Bulle',4,'La fusion nucléaire sans risque !',3);
INSERT INTO "equipment" VALUES(15,'La Colère de la Daronne',4,'Quand elle t''appelle par tous tes prénoms ET ton nom de famille, tu sais que ça va chier.',3);
INSERT INTO "equipment" VALUES(16,'Plancha caramba',2,'Old El Paso, tacos y sombreros.',2);
INSERT INTO "equipment" VALUES(17,'Cocotte-milliseconde Pouftroptard',1,'Là, c''est trop tard...',2);
INSERT INTO "equipment" VALUES(18,'Alambic H.i.C.',2,'Fourni avec une boîte de 10 alcootests !',2);
INSERT INTO "equipment" VALUES(19,'Centrifugeur Gerboulex',2,'Peut aussi servir d''essoreur à salade.',2);
INSERT INTO "equipment" VALUES(20,'Ampoule à décanter Paul Bocal',1,'"Bien agiter - Laisser reposer." - Manuel d''éducation positive.',2);
INSERT INTO "equipment" VALUES(21,'Pipotron',4,'Virtuosité moléculaire, abnégation expérimentale et langue de bois.',2);
INSERT INTO "equipment" VALUES(22,'Plaque à induction',3,'12 feux, 18 tailles et 25 diamètres.',2);
INSERT INTO "equipment" VALUES(23,'Easy-Filtration®',3,'Une solution complète pour toutes vos expérimentations !',2);
INSERT INTO "equipment" VALUES(24,'Sphère flottante SpaceX',3,'Les sons pleine balle de Katy Perry font partie intégrante du processus infra-atomique résonnanciel de transmutation.',2);
CREATE TABLE equipment_categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "equipment_categories" VALUES(1,'Instrument');
INSERT INTO "equipment_categories" VALUES(2,'Creuset');
INSERT INTO "equipment_categories" VALUES(3,'Feu');
INSERT INTO "equipment_categories" VALUES(4,'Contenant');
CREATE TABLE equipment_craft (
    equipment_id INTEGER,
    ingredient_id INTEGER,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (equipment_id, ingredient_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
INSERT INTO "equipment_craft" VALUES(1,15,1);
INSERT INTO "equipment_craft" VALUES(1,17,3);
INSERT INTO "equipment_craft" VALUES(2,16,2);
INSERT INTO "equipment_craft" VALUES(3,3,10);
INSERT INTO "equipment_craft" VALUES(3,15,10);
INSERT INTO "equipment_craft" VALUES(5,17,10);
INSERT INTO "equipment_craft" VALUES(5,3,2);
INSERT INTO "equipment_craft" VALUES(4,17,5);
INSERT INTO "equipment_craft" VALUES(4,3,1);
CREATE TABLE ingredient_affinities (
    ingredient_id INTEGER,
    affinity_id INTEGER,
    value REAL,
    PRIMARY KEY (ingredient_id, affinity_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (affinity_id) REFERENCES affinities(id)
);
INSERT INTO "ingredient_affinities" VALUES(9,4,1.0);
INSERT INTO "ingredient_affinities" VALUES(2,5,0.6);
INSERT INTO "ingredient_affinities" VALUES(2,2,0.4);
INSERT INTO "ingredient_affinities" VALUES(7,1,0.8);
INSERT INTO "ingredient_affinities" VALUES(7,4,0.2);
INSERT INTO "ingredient_affinities" VALUES(11,6,1.0);
INSERT INTO "ingredient_affinities" VALUES(6,6,0.4);
INSERT INTO "ingredient_affinities" VALUES(6,2,0.6);
INSERT INTO "ingredient_affinities" VALUES(10,6,0.5);
INSERT INTO "ingredient_affinities" VALUES(10,2,0.3);
INSERT INTO "ingredient_affinities" VALUES(10,5,0.2);
INSERT INTO "ingredient_affinities" VALUES(3,6,1.0);
INSERT INTO "ingredient_affinities" VALUES(1,1,0.7);
INSERT INTO "ingredient_affinities" VALUES(1,5,0.3);
INSERT INTO "ingredient_affinities" VALUES(4,6,0.6);
INSERT INTO "ingredient_affinities" VALUES(4,2,0.4);
INSERT INTO "ingredient_affinities" VALUES(13,4,0.3);
INSERT INTO "ingredient_affinities" VALUES(13,5,0.7);
INSERT INTO "ingredient_affinities" VALUES(5,6,0.6);
INSERT INTO "ingredient_affinities" VALUES(5,3,0.3);
INSERT INTO "ingredient_affinities" VALUES(5,2,0.1);
INSERT INTO "ingredient_affinities" VALUES(12,3,0.5);
INSERT INTO "ingredient_affinities" VALUES(12,1,0.1);
INSERT INTO "ingredient_affinities" VALUES(12,5,0.4);
INSERT INTO "ingredient_affinities" VALUES(8,3,0.5);
INSERT INTO "ingredient_affinities" VALUES(8,6,0.3);
INSERT INTO "ingredient_affinities" VALUES(8,2,0.2);
INSERT INTO "ingredient_affinities" VALUES(14,2,1.0);
INSERT INTO "ingredient_affinities" VALUES(17,5,0.5);
INSERT INTO "ingredient_affinities" VALUES(17,1,0.5);
INSERT INTO "ingredient_affinities" VALUES(16,3,1.0);
INSERT INTO "ingredient_affinities" VALUES(15,1,0.5);
INSERT INTO "ingredient_affinities" VALUES(15,2,0.5);
INSERT INTO "ingredient_affinities" VALUES(18,6,0.7);
INSERT INTO "ingredient_affinities" VALUES(18,4,0.3);
INSERT INTO "ingredient_affinities" VALUES(19,3,0.8);
INSERT INTO "ingredient_affinities" VALUES(19,6,0.2);
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    level INTEGER,
    rarity_id INTEGER,

    FOREIGN KEY (rarity_id) REFERENCES rarities(id)
);
INSERT INTO "ingredients" VALUES(1,'Soie d''araignée','Brille légèrement.',1,2);
INSERT INTO "ingredients" VALUES(2,'Plume noire','Une plume noire avec des tons bleutés.',1,1);
INSERT INTO "ingredients" VALUES(3,'Bûche','Une bûche. Pratique pour construire des trucs.',1,1);
INSERT INTO "ingredients" VALUES(4,'Champignon sombre','Un champignon noir aux propriétés étranges.',1,1);
INSERT INTO "ingredients" VALUES(5,'Pomme rouge','Une pomme rouge, on dirait de la Red Delicious... Est ce qu''elle est bio ?',1,1);
INSERT INTO "ingredients" VALUES(6,'Mandragore','On dirait un bébé Reborn. Et pas un mignon.',1,3);
INSERT INTO "ingredients" VALUES(7,'Pierre de lune','Apporte douceur et tolérance aux gens cons et bornés. Mieux que de manger des carottes !',1,3);
INSERT INTO "ingredients" VALUES(8,'Bolet infernal','Tristement célèbre pour sa toxicité et son odeur nauséabonde.',1,3);
INSERT INTO "ingredients" VALUES(9,'Eau claire','La base pour toutes les préparations !',1,1);
INSERT INTO "ingredients" VALUES(10,'Clochette des brumes','Les fées adorent s''en servir comme chapeau, mais évite de mettre ton doigt dedans. Conseil d''ami.',1,2);
INSERT INTO "ingredients" VALUES(11,'Rhubarbe des bois','Délicieuse en confiture ou dans une tarte.',1,2);
INSERT INTO "ingredients" VALUES(12,'Poil de renard','Une belle touffe de poils flamboyante.',1,1);
INSERT INTO "ingredients" VALUES(13,'Scarabée bleu','Très bel insecte, fortement apprécié des grenouilles pour sa finesse gustative et son croquant inimitable.',1,2);
INSERT INTO "ingredients" VALUES(14,'Dent de loup','Pas aussi bien qu''une dent de requin, mais on fera avec.',1,1);
INSERT INTO "ingredients" VALUES(15,'Pierre','Pierre qui roule n''amasse pas mousse.',1,1);
INSERT INTO "ingredients" VALUES(16,'Minerai de cuivre','Chouette, un caillou qui brille !',1,2);
INSERT INTO "ingredients" VALUES(17,'Sable fin','Il devait y avoir un cours d''eau ici.',1,1);
INSERT INTO "ingredients" VALUES(18,'Menthe verte','La vie mettra de la menthe sur ton chemin. À toi de décider si tu en fais du thé ou des mojitos...',1,1);
INSERT INTO "ingredients" VALUES(19,'Sauge rouge','Qui a de la sauge dans son jardin, n’a pas besoin de médecin.',1,2);
CREATE TABLE inventory (
        ingredient_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
INSERT INTO "inventory" VALUES(1,2);
INSERT INTO "inventory" VALUES(2,3);
INSERT INTO "inventory" VALUES(4,8);
INSERT INTO "inventory" VALUES(6,1);
INSERT INTO "inventory" VALUES(7,2);
INSERT INTO "inventory" VALUES(8,16);
INSERT INTO "inventory" VALUES(9,1);
INSERT INTO "inventory" VALUES(12,9);
INSERT INTO "inventory" VALUES(13,2);
INSERT INTO "inventory" VALUES(14,4);
INSERT INTO "inventory" VALUES(16,2);
CREATE TABLE mixing_tools (
    equipment_id INTEGER PRIMARY KEY,
    capacity INTEGER,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);
INSERT INTO "mixing_tools" VALUES(1,2);
INSERT INTO "mixing_tools" VALUES(6,3);
INSERT INTO "mixing_tools" VALUES(7,4);
INSERT INTO "mixing_tools" VALUES(8,5);
INSERT INTO "mixing_tools" VALUES(9,6);
CREATE TABLE rarities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL
, weight REAL);
INSERT INTO "rarities" VALUES(1,'commun','white',10.0);
INSERT INTO "rarities" VALUES(2,'inhabituel','green',6.0);
INSERT INTO "rarities" VALUES(3,'rare','blue',3.0);
INSERT INTO "rarities" VALUES(4,'épique','purple',1.0);
CREATE TABLE recipe_discovery (
        recipe_id INTEGER,
        number_of_ingredients INTEGER NOT NULL,
        affinity_id INTEGER,
        value REAL,
        PRIMARY KEY (recipe_id, affinity_id),
        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (affinity_id) REFERENCES affinities(id)
    );
CREATE TABLE recipe_types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "recipe_types" VALUES(1,'Potion');
INSERT INTO "recipe_types" VALUES(2,'Élixir');
INSERT INTO "recipe_types" VALUES(3,'Pentagramme');
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    description TEXT,
    effect TEXT,
    rarity_id INTEGER,
    fire_equipment_id INTEGER,
    melting_pot_equipment_id INTEGER,
    FOREIGN KEY (type_id) REFERENCES recipe_types(id),
    FOREIGN KEY (target_id) REFERENCES targets(id),
    FOREIGN KEY (rarity_id) REFERENCES rarities(id),
    FOREIGN KEY (fire_equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (melting_pot_equipment_id) REFERENCES equipment(id)
);
INSERT INTO "recipes" VALUES(1,'Potion de soin',1,1,'Un soin instantané goût framboise.','+80 points de vie',1,NULL,NULL);
INSERT INTO "recipes" VALUES(2,'Potion de mana',1,1,'Une récupération de mana instantanée goût Kola Koala.','+80 points de mana',1,NULL,NULL);
INSERT INTO "recipes" VALUES(3,'Potion de puissance',1,1,'Pétillante en bouche, parfaite pour péter des gueules.','+10 puissance pendant 3 tours',2,NULL,NULL);
INSERT INTO "recipes" VALUES(4,'Potion Source de vie',1,3,'Un soin chaleureux et convivial, comme les douches du rugby.','+20 points de vie pendant 3 tours',2,NULL,NULL);
CREATE TABLE targets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "targets" VALUES(1,'Soi');
INSERT INTO "targets" VALUES(2,'Allié');
INSERT INTO "targets" VALUES(3,'Équipe');
INSERT INTO "targets" VALUES(4,'Ennemi');
INSERT INTO "targets" VALUES(5,'Tous les ennemis');
COMMIT;
