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
CREATE TABLE container_inventory (
    equipment_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);
INSERT INTO "container_inventory" VALUES(4,2);
INSERT INTO "container_inventory" VALUES(5,2);
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
INSERT INTO "equipment" VALUES(9,'Thermomix 9000 DolbyTHX',4,'Si vous pouvez tâcher moyen de vous éloigner de vingt-cinq pieds, bon pieds hein, parce que ça va gicler un peu.',1);
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
INSERT INTO "equipment" VALUES(25,'Flasque souple',1,'En silicone magique recyclable.',4);
INSERT INTO "equipment" VALUES(26,'Thermos de chantier',2,'Récipient isotherme ultra-robuste conçu pour maintenir les boissons chaudes ou froides dans des conditions de travail difficiles.',4);
INSERT INTO "equipment" VALUES(27,'Flacon en cristal ciselé',2,'Un bel ouvrage de la marque prestigieuse Pierre Brochant.',4);
INSERT INTO "equipment" VALUES(28,'Mini baril plombé',1,'Idéal pour les mélanges agités.',4);
INSERT INTO "equipment" VALUES(29,'Bocal à anchois',1,'Plébiscité par Joseph d''Arimathie pour sa polyvalence et sa praticité.',4);
INSERT INTO "equipment" VALUES(30,'Flasque Metal Gear Solid',3,'En métal hypoallergénique, non testé sur les animaux.',4);
INSERT INTO "equipment" VALUES(31,'Tonnelet en bois-sorcier',3,'Son bois précieux issu du commerce équitable conserve tous les bienfaits de votre boisson.',4);
INSERT INTO "equipment" VALUES(32,'Poche à perfusion',3,'Pour toute administration intraveineuse de substance à diffusion lente.',4);
INSERT INTO "equipment" VALUES(33,'Tireuse à bière',4,'Sert votre potion ou élixir à pression optimale.',4);
INSERT INTO "equipment" VALUES(34,'Flacon Oeil-de-Dragon',4,'Baisse les yeux.',4);
INSERT INTO "equipment" VALUES(35,'Cuir tanné',1,'Non vegan. Provenance couverte par notre clause de confidentialité.',4);
INSERT INTO "equipment" VALUES(36,'Parchemin maudit',1,'Issu de la synergie de nos chaînes de montage hi-tech et du savoir-faire millénaire de nos partenaires en poisse et emmerdements. ',4);
INSERT INTO "equipment" VALUES(37,'Serviette de table',1,'En coton bio éco-sourcé.',4);
INSERT INTO "equipment" VALUES(38,'Carré de soie',1,'Son prix n''a d''égal que le prestige de la grande maison qui le fabrique.',4);
INSERT INTO "equipment" VALUES(39,'Affiche électorale',2,'Tous bords politiques disponibles, sélectionnés selon le niveau d''enculade des promesses de campagne. ',4);
INSERT INTO "equipment" VALUES(40,'Papyrus',2,'En provenance directe de nos pyramides, extra-fraîcheur garantie !',4);
INSERT INTO "equipment" VALUES(41,'Notice de montage IKEA',3,'Il restera toujours une vis à la fin.',4);
INSERT INTO "equipment" VALUES(42,'Feuille de Bananarama',3,'Issue de la cueillette intensive et raisonnée par nos bulldozers magiques.',4);
INSERT INTO "equipment" VALUES(43,'Cloison de logement social',4,'D''une finesse inégalée !',4);
INSERT INTO "equipment" VALUES(44,'Contrat d''assurance',4,'Sélectionné avec soin selon le degré de putasserie des mentions en petits caractères et des clauses suspensives.',4);
INSERT INTO "equipment" VALUES(45,'Plan dimensionnel',4,'Provenance 99,9 % de dimensions alternatives. Possibles traces d''arachides, de noix ou d''amandes.',4);
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
CREATE TABLE ingredient_affinities (
    ingredient_id INTEGER,
    affinity_id INTEGER,
    value REAL,
    PRIMARY KEY (ingredient_id, affinity_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (affinity_id) REFERENCES affinities(id)
);
INSERT INTO "ingredient_affinities" VALUES(9,4,1.0);
INSERT INTO "ingredient_affinities" VALUES(7,1,0.8);
INSERT INTO "ingredient_affinities" VALUES(7,4,0.2);
INSERT INTO "ingredient_affinities" VALUES(10,6,0.5);
INSERT INTO "ingredient_affinities" VALUES(10,2,0.3);
INSERT INTO "ingredient_affinities" VALUES(10,5,0.2);
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
INSERT INTO "ingredient_affinities" VALUES(11,4,0.6);
INSERT INTO "ingredient_affinities" VALUES(11,6,0.4);
INSERT INTO "ingredient_affinities" VALUES(3,6,0.8);
INSERT INTO "ingredient_affinities" VALUES(3,4,0.2);
INSERT INTO "ingredient_affinities" VALUES(20,4,0.9);
INSERT INTO "ingredient_affinities" VALUES(20,5,0.1);
INSERT INTO "ingredient_affinities" VALUES(2,2,0.3);
INSERT INTO "ingredient_affinities" VALUES(2,5,0.6);
INSERT INTO "ingredient_affinities" VALUES(2,1,0.1);
INSERT INTO "ingredient_affinities" VALUES(21,6,0.5);
INSERT INTO "ingredient_affinities" VALUES(21,3,0.3);
INSERT INTO "ingredient_affinities" VALUES(21,2,0.2);
INSERT INTO "ingredient_affinities" VALUES(6,2,0.6);
INSERT INTO "ingredient_affinities" VALUES(6,1,0.4);
INSERT INTO "ingredient_affinities" VALUES(22,2,0.6);
INSERT INTO "ingredient_affinities" VALUES(22,4,0.4);
INSERT INTO "ingredient_affinities" VALUES(23,5,0.6);
INSERT INTO "ingredient_affinities" VALUES(23,6,0.2);
INSERT INTO "ingredient_affinities" VALUES(23,3,0.2);
INSERT INTO "ingredient_affinities" VALUES(24,1,0.6);
INSERT INTO "ingredient_affinities" VALUES(24,6,0.4);
INSERT INTO "ingredient_affinities" VALUES(25,2,0.6);
INSERT INTO "ingredient_affinities" VALUES(25,6,0.4);
INSERT INTO "ingredient_affinities" VALUES(27,6,1.0);
INSERT INTO "ingredient_affinities" VALUES(26,6,1.0);
INSERT INTO "ingredient_affinities" VALUES(28,6,0.5);
INSERT INTO "ingredient_affinities" VALUES(28,3,0.5);
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
INSERT INTO "ingredients" VALUES(20,'Écaille de poisson ailé','Ce poisson possède des nageoires pectorales très développées qui lui permettent de faire des vols planés hors de l''eau.',1,1);
INSERT INTO "ingredients" VALUES(21,'Graine de citrouille','Ptet''y va t''pousser un carrosse !',1,1);
INSERT INTO "ingredients" VALUES(22,'Larme de sorcière','Cette plante tombante pousse au bord des mares d''eau stagnante.',1,2);
INSERT INTO "ingredients" VALUES(23,'Cendre de feu follet','Forme des petits monticules légèrement rougeoyants.',1,3);
INSERT INTO "ingredients" VALUES(24,'Muguettine','Ses jolies clochettes argentées tintent les nuits de pleine lune.',1,2);
INSERT INTO "ingredients" VALUES(25,'Aconit','Aussi appelé napel ou tue-loup. Suis un peu tes cours de potions !',1,2);
INSERT INTO "ingredients" VALUES(26,'Pavlovnia','Cette plante a de très bons réflexes.',1,3);
INSERT INTO "ingredients" VALUES(27,'Vigne catcheuse','L''oeil du tigre. Tin-tin-tin, tin-tin-tiiiiinnnnnnn...',1,3);
INSERT INTO "ingredients" VALUES(28,'Baies piquantes','Ça arrache un peu.',1,1);
CREATE TABLE inventory (
        ingredient_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
INSERT INTO "inventory" VALUES(1,5);
INSERT INTO "inventory" VALUES(2,11);
INSERT INTO "inventory" VALUES(3,16);
INSERT INTO "inventory" VALUES(4,42);
INSERT INTO "inventory" VALUES(5,11);
INSERT INTO "inventory" VALUES(6,8);
INSERT INTO "inventory" VALUES(7,2);
INSERT INTO "inventory" VALUES(8,22);
INSERT INTO "inventory" VALUES(9,16);
INSERT INTO "inventory" VALUES(10,15);
INSERT INTO "inventory" VALUES(11,26);
INSERT INTO "inventory" VALUES(12,31);
INSERT INTO "inventory" VALUES(13,5);
INSERT INTO "inventory" VALUES(14,14);
INSERT INTO "inventory" VALUES(15,17);
INSERT INTO "inventory" VALUES(16,11);
INSERT INTO "inventory" VALUES(17,13);
INSERT INTO "inventory" VALUES(18,13);
INSERT INTO "inventory" VALUES(19,8);
INSERT INTO "inventory" VALUES(20,2);
INSERT INTO "inventory" VALUES(21,11);
INSERT INTO "inventory" VALUES(22,3);
INSERT INTO "inventory" VALUES(23,1);
INSERT INTO "inventory" VALUES(24,6);
INSERT INTO "inventory" VALUES(25,14);
INSERT INTO "inventory" VALUES(26,0);
INSERT INTO "inventory" VALUES(27,8);
INSERT INTO "inventory" VALUES(28,1);
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
CREATE TABLE player_equipment (
    equipment_id INTEGER PRIMARY KEY,
    crafted INTEGER NOT NULL DEFAULT 0 CHECK (crafted IN (0, 1)),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);
INSERT INTO "player_equipment" VALUES(2,1);
INSERT INTO "player_equipment" VALUES(3,1);
CREATE TABLE player_recipes (
    recipe_id INTEGER PRIMARY KEY,
    crafted INTEGER NOT NULL DEFAULT 0
    	CHECK (crafted IN (0, 1)),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
INSERT INTO "player_recipes" VALUES(1,1);
INSERT INTO "player_recipes" VALUES(2,0);
INSERT INTO "player_recipes" VALUES(3,0);
INSERT INTO "player_recipes" VALUES(5,1);
INSERT INTO "player_recipes" VALUES(6,0);
INSERT INTO "player_recipes" VALUES(7,0);
INSERT INTO "player_recipes" VALUES(8,0);
INSERT INTO "player_recipes" VALUES(9,0);
INSERT INTO "player_recipes" VALUES(10,0);
INSERT INTO "player_recipes" VALUES(11,0);
INSERT INTO "player_recipes" VALUES(12,0);
INSERT INTO "player_recipes" VALUES(13,0);
CREATE TABLE product_inventory (
    recipe_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
INSERT INTO "product_inventory" VALUES(1,1);
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
INSERT INTO "recipe_discovery" VALUES(1,2,6,0.6);
INSERT INTO "recipe_discovery" VALUES(1,2,4,0.4);
INSERT INTO "recipe_discovery" VALUES(2,2,5,0.4);
INSERT INTO "recipe_discovery" VALUES(2,2,4,0.6);
INSERT INTO "recipe_discovery" VALUES(3,2,3,1.0);
INSERT INTO "recipe_discovery" VALUES(4,2,1,0.2);
INSERT INTO "recipe_discovery" VALUES(4,2,6,0.4);
INSERT INTO "recipe_discovery" VALUES(4,2,4,0.4);
INSERT INTO "recipe_discovery" VALUES(5,3,6,0.6);
INSERT INTO "recipe_discovery" VALUES(5,3,4,0.4);
INSERT INTO "recipe_discovery" VALUES(6,3,3,0.5);
INSERT INTO "recipe_discovery" VALUES(6,3,6,0.5);
INSERT INTO "recipe_discovery" VALUES(8,2,2,0.4);
INSERT INTO "recipe_discovery" VALUES(8,2,1,0.3);
INSERT INTO "recipe_discovery" VALUES(8,2,5,0.3);
INSERT INTO "recipe_discovery" VALUES(11,2,6,0.4);
INSERT INTO "recipe_discovery" VALUES(11,2,1,0.3);
INSERT INTO "recipe_discovery" VALUES(11,2,2,0.3);
INSERT INTO "recipe_discovery" VALUES(13,2,3,0.5);
INSERT INTO "recipe_discovery" VALUES(13,2,5,0.3);
INSERT INTO "recipe_discovery" VALUES(13,2,6,0.2);
INSERT INTO "recipe_discovery" VALUES(12,2,2,0.5);
INSERT INTO "recipe_discovery" VALUES(12,2,6,0.3);
INSERT INTO "recipe_discovery" VALUES(12,2,4,0.2);
INSERT INTO "recipe_discovery" VALUES(9,2,3,0.4);
INSERT INTO "recipe_discovery" VALUES(9,2,6,0.4);
INSERT INTO "recipe_discovery" VALUES(9,2,2,0.2);
INSERT INTO "recipe_discovery" VALUES(10,2,2,0.8);
INSERT INTO "recipe_discovery" VALUES(10,2,1,0.2);
INSERT INTO "recipe_discovery" VALUES(7,2,6,1.0);
CREATE TABLE recipe_ingredients (
    recipe_id INTEGER,
    ingredient_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)

);
INSERT INTO "recipe_ingredients" VALUES(1,9,3);
INSERT INTO "recipe_ingredients" VALUES(1,18,1);
INSERT INTO "recipe_ingredients" VALUES(2,9,2);
INSERT INTO "recipe_ingredients" VALUES(2,15,2);
INSERT INTO "recipe_ingredients" VALUES(3,19,2);
INSERT INTO "recipe_ingredients" VALUES(3,3,1);
INSERT INTO "recipe_ingredients" VALUES(4,1,2);
INSERT INTO "recipe_ingredients" VALUES(4,18,4);
INSERT INTO "recipe_ingredients" VALUES(7,15,2);
INSERT INTO "recipe_ingredients" VALUES(7,3,3);
INSERT INTO "recipe_ingredients" VALUES(9,21,3);
INSERT INTO "recipe_ingredients" VALUES(9,19,1);
INSERT INTO "recipe_ingredients" VALUES(9,8,1);
INSERT INTO "recipe_ingredients" VALUES(8,17,3);
INSERT INTO "recipe_ingredients" VALUES(8,2,5);
INSERT INTO "recipe_ingredients" VALUES(8,10,1);
INSERT INTO "recipe_ingredients" VALUES(10,14,3);
INSERT INTO "recipe_ingredients" VALUES(10,4,2);
INSERT INTO "recipe_ingredients" VALUES(10,6,1);
INSERT INTO "recipe_ingredients" VALUES(12,8,1);
INSERT INTO "recipe_ingredients" VALUES(12,5,2);
INSERT INTO "recipe_ingredients" VALUES(11,3,3);
INSERT INTO "recipe_ingredients" VALUES(11,15,2);
INSERT INTO "recipe_ingredients" VALUES(11,7,1);
INSERT INTO "recipe_ingredients" VALUES(13,16,1);
INSERT INTO "recipe_ingredients" VALUES(13,19,2);
INSERT INTO "recipe_ingredients" VALUES(7,1,3);
INSERT INTO "recipe_ingredients" VALUES(5,9,5);
INSERT INTO "recipe_ingredients" VALUES(5,11,4);
INSERT INTO "recipe_ingredients" VALUES(5,26,3);
INSERT INTO "recipe_ingredients" VALUES(5,24,1);
INSERT INTO "recipe_ingredients" VALUES(6,27,2);
INSERT INTO "recipe_ingredients" VALUES(6,25,3);
CREATE TABLE recipe_products (
    recipe_id INTEGER NOT NULL,
    product_recipe_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,

    PRIMARY KEY (recipe_id, product_recipe_id),

    FOREIGN KEY (recipe_id)
        REFERENCES recipes(id),

    FOREIGN KEY (product_recipe_id)
        REFERENCES recipes(id)
);
INSERT INTO "recipe_products" VALUES(5,1,1);
INSERT INTO "recipe_products" VALUES(6,7,1);
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
    melting_pot_equipment_id INTEGER, container_equipment_id INTEGER
    REFERENCES equipment(id),
    FOREIGN KEY (type_id) REFERENCES recipe_types(id),
    FOREIGN KEY (target_id) REFERENCES targets(id),
    FOREIGN KEY (rarity_id) REFERENCES rarities(id),
    FOREIGN KEY (fire_equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (melting_pot_equipment_id) REFERENCES equipment(id)
);
INSERT INTO "recipes" VALUES(1,'Potion de soin',1,1,'Un soin instantané goût framboise.','+80 points de vie',1,NULL,NULL,4);
INSERT INTO "recipes" VALUES(2,'Potion de mana',1,1,'Une récupération de mana instantanée goût Kola Koala.','+80 points de mana',1,NULL,NULL,4);
INSERT INTO "recipes" VALUES(3,'Potion de puissance',1,1,'Pétillante en bouche, parfaite pour péter des gueules.','+10 puissance pendant 3 tours',2,NULL,NULL,4);
INSERT INTO "recipes" VALUES(4,'Potion Source de vie',1,3,'Un soin chaleureux et convivial, comme les douches du rugby.','+20 points de vie pendant 3 tours',2,NULL,NULL,5);
INSERT INTO "recipes" VALUES(5,'Grande potion de soin',1,3,'L''effet d''un cri de guerre à Fort Boyard, l''hydratation en plus !','+100 points de vie',3,3,2,5);
INSERT INTO "recipes" VALUES(6,'Potion de peau de cuir',1,1,'Vous êtes maintenant un vrai dur à cuir ! ','+20 points de défense pendant 3 tours',3,3,2,5);
INSERT INTO "recipes" VALUES(7,'Potion de défense',1,1,'Pour encaisser les coups comme un bonhomme.','+10 points de défense pendant 2 tours',1,NULL,NULL,4);
INSERT INTO "recipes" VALUES(8,'Élixir de vitesse',2,1,'Cours Forest, cours !','+5 points de vitesse pendant 15 minutes de jeu',1,NULL,NULL,25);
INSERT INTO "recipes" VALUES(9,'Élixir de peau de dragon',2,1,'Acide hyaluronique + rétinol A.','+8 points de défense pendant 15 minutes de jeu',1,NULL,NULL,4);
INSERT INTO "recipes" VALUES(10,'Pentagramme de Terreur',3,4,'BOUH.','Applique Peur pendant 2 tours',1,NULL,NULL,37);
INSERT INTO "recipes" VALUES(11,'Pentagramme de la Tatane',3,4,'Tu l''as pas volée, celle-là !','Applique Stun pendant 2 tours',2,3,2,35);
INSERT INTO "recipes" VALUES(12,'Pentagramme de la Conserve Périmée',3,4,'Boah, allez, je goûte...','Applique Poison pendant 2 tours',1,NULL,NULL,37);
INSERT INTO "recipes" VALUES(13,'Pentagramme du Pyromane',3,4,'Une allumette, charlipopette...','Applique Brûlure pendant 2 tours',1,NULL,NULL,37);
CREATE TABLE shop_inventory (
    recipe_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
INSERT INTO "shop_inventory" VALUES(5,1);
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
