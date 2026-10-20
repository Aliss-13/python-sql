import random

import player_game.game_state

from display.display_utils import YELLOW, RESET, CYAN, COLORS
from player_game.inventory import add_ingredient_to_inventory


def trigger_blending_accident(cursor, connection, blending_ingredients, capacity):

    accidents = [
        #advertising_interference,
        #lambda: crackling_explosion(cursor, connection),
        lambda: transformation_of_matter(cursor, connection, blending_ingredients),
        #lambda: gemino_gemini(cursor, connection, blending_ingredients),
        #lambda: surprise_preparation(cursor, connection, capacity),
        #hes_alive,
        #taxes_and_fuckeries
    ]

    if player_game.game_state.active_event is not None:
        return

    print("⚠️ ACCIDENT ALCHIMIQUE ⚠️")
    print()

    random.choice(accidents)()

#------------------------------------------- Gestion temporalité des évènements textuels --------------------------------------------------
#                                                    advertising_interference
#                                                       taxes_and_fuckeries
#                                                             hes_alive

def start_temporary_event(dialogue_function, end_message):

    if player_game.game_state.active_event is not None:
        return False
    
    player_game.game_state.active_event = dialogue_function
    player_game.game_state.event_start_tick = player_game.game_state.game_tick
    player_game.game_state.last_event_tick = player_game.game_state.game_tick
    player_game.game_state.event_end_message = end_message

    print(dialogue_function())
    return True


def tick_temporary_event(game_tick):

    EVENT_DURATION = 12
    EVENT_INTERVAL = 3

    if player_game.game_state.active_event is None:
        return

    elapsed = game_tick - player_game.game_state.event_start_tick

    if elapsed >= EVENT_DURATION:
        print(player_game.game_state.event_end_message)

        player_game.game_state.active_event = None
        player_game.game_state.event_start_tick = None
        player_game.game_state.last_event_tick = None
        player_game.game_state.event_end_message = None
        return

    if game_tick - player_game.game_state.last_event_tick >= EVENT_INTERVAL:
        print(player_game.game_state.active_event())
        player_game.game_state.last_event_tick = game_tick

#------------------------------------------------- Interférence publicitaire --------------------------------------------------------------

def advertising_interference():

    print("📡 INTERFÉRENCE PUBLICITAIRE ARCANIQUE DÉTECTÉE !")
    print("Une fréquence commerciale parasite votre laboratoire...")
    start_temporary_event(random_advertising_interference, "✨ Le signal publicitaire arcanique s'est dissipé.")


def random_advertising_interference():
    text = random.choice(ADVERTISING_INTERFERENCE)
    return text


ADVERTISING_INTERFERENCE = [
    "📻 « Certaines personnes sont gênantes pour vos affaires ? Le « Transmut-O-Plomb » de Roger Bacon Logistics, c'est LA solution ! "
    "\nJuste avant votre procès, le témoin est livré sur un chantier et coulé dans le béton le plus frais ! "
    "\nPas de trace, pas de paperasse ! »"
    "\n(Chorale joyeuse 🎶) : « Avec Roger Bacon Logistics, ton business devient fantastics ! »",
    
    "📻 « Chez Maurice Bark Assurances, on sait que la vie d’alchimiste réserve des surprises. Vous vouliez changer votre vieux grille-pain "
    "\nen lingot d'or, mais vous avez glissé et transmuté votre belle-mère en table basse en teck ? » "
    "\n(Bruit de flûte à coulisse et cri de vieille dame) "
    "\n« Pas de panique ! Notre forfait Responsabilité Civile Esotérique prend tout en charge ! "
    "\nOn rembourse les frais de ponçage et on livre gratuitement une nappe assortie ! » 🎶",
     
    "📻 « Faire l'épicerie te prend trois heures ?! T'en as marre de slalomer entre les p'tits vieux qui bloquent le rayon des yogourts ?! "
    "\nPouftroptard a la solution alchimique ultime : le spray Compact'Achat Express ! »"
    "\n(Bruit de pshiiit, suivi d'une grosse explosion magique 💥)"
    "\n« C'est simple : tu rentres dans le magasin, tu pshiiites ta liste, et BAM ! Tout le supermarché se transforme instantanément "
    "\nen une seule pilule compacte qui goûte le carton ! Tu l'avales à la caisse et t'as plus faim pour les six prochains mois ! »"
    "\n(Ding de caisse enregistreuse 💰)",

    "📻 « Vous êtes célibataire, peu charismatique et habitez seul avec Maman ? Montrez que vous en avez sous le capot ! "
    "\nSpaceX Broomsticks présente le TornadoSharkLux 3000, le premier balai volant TRÈS HAUTE TECHNOLOGIE ! » "
    "\n(💨 Bruit de vouschhhhh suivi d’un bang supersonique 💥) "
    "\n« Avec son manche à balai en langue de bois, fusionné avec de l'antimatière et de la haine pure, vous passez de 0 à 100 km/h en deux microsecondes !"
    "\nLivré avec lancer de culottes, jalousie de votre entourage et promotion canapé. »"
    "\n(Voix qui parle très vite et tout bas)"
    "\n« Attention : pas de garantie de cet ordre, lancer de canapé, promotion de votre entourage et jalousie de culottes sont possibles "
    "\nà cause des effets de la haine pure. Parlez-en à votre Maman. »"
      ]

#------------------------------------------------- Il est vivant ! --------------------------------------------------------------

def hes_alive():

    print("🐙 IL EST VIVANT !")
    print("Oh, mais il parle...")
    print()

    companions = {
    "La Commère astrale": random_astral_gossip_dialogue,
    "Le Conseiller catastrophique": random_catastrophic_advisor_dialogue,
    "Le Bouffon dimensionnel": random_dimensional_comic_dialogue
    }

    name, dialogue_function = random.choice(list(companions.items()))

    print(f"✨ Vous avez invoqué {YELLOW}{name}{RESET} !")
    print()
    start_temporary_event(dialogue_function, "✨ Il est reparti... Ouf.")


def random_astral_gossip_dialogue():
    text = random.choice(ASTRAL_GOSSIP)
    return text

def random_catastrophic_advisor_dialogue():
    text = random.choice(CATASTROPHIC_ADVISOR)
    return text

def random_dimensional_comic_dialogue():
    text = random.choice(DIMENSIONAL_COMIC)
    return text


ASTRAL_GOSSIP = [
    "🤫 « Il paraît que Mélusine Flamel a rompu avec le prince Hermès Cosmopolite. Une sombre histoire de massage de pieds par "
    "\nle sulfureux Ash D'Anfers. Il les aura toutes, nos quarantenaires de l'Alambic-set. En même temps il est si bel homme, "
    "\ndifficile de résister. »",

    "🤫 « Non, tu sais pas ce que m'a confié Archix l'archiviste ? Il a vu passer des papyrus pour de la lingerie en soie d'araignée venant "
    "\nde chez Gigi Hendrix. Mais SI ! Oui, tout le monde la croyait anéantie par la perte de son mari, le corps est encore chaud... »", 

    "🤫 « Sais-tu ce qu'a enendu Papotine au Nessie-Café tout à l'heure ? Roger Bacon Logistics aurait de gros problèmes financiers. "
    "\nUn audit de la DDDP qui aurait mal tourné... Oui, la DDDP, la Direction Dimensionnelle des Deniers Publics... "
    "\nTu connais pas ? Tu devrais. Je dis ça je dis rien, hein. »",

    "🤫 « J'ai vu le voisin acheter un exemplaire de 'Cuisses légères et Vesses à vent' au kiosque. Franchement il n'est pas discret. "
    "\nIl pourrait aller sur InterMa comme tout le monde... Inter Maille Élémentaire enfin ! Tu y vas pour tes commandes fournisseur, "
    "\nfaut te mettre à la page sur le langage des jeunes ma vieille ! »",

    "🤫 « ... et elle l'a surpris au lit avec une chaise ! Une chaise, tu te rends compte ? Oui, le modèle Henriksdal. »",

    "🤫 « ... Je l'ai vu dans le Magibus, il avait l'air é-pui-sé. Depuis qu'il est devenu végétarien, ça ne lui réussit pas. Non mais un "
    "\nvampire végétarien, avoue que ça ne ressemble à rien, c'est comme une tartiflette sans fromage ou un contrat d'assurance honnête... »",
    ]

CATASTROPHIC_ADVISOR =  [
    "😎 « Franchement tu devrais mettre des billes dans Roger Bacon Logistics, c'est une valeur sûre ! »",
    "😎 « Pourquoi tu refuses les invitations du voisin ? Il a l'air d'être un mec super, et tu vas pas en rajeunissant ma grande. »",
    "😎 « Tu devrais parler de ta super idée à Papotine. Elle est discrète et de bon conseil. »", 
    "😎 « T'enlèves un zéro du Compta-Grim, oui là, sur cette ligne. Tranquille Émile ! Mon pote Randall fait ça tout le temps. »",
    "😎 « Je sens que l'élixir d'invisibilité dans le noir total va être un banger cette année. »",
    "😎 « Pourquoi tu refais pas du stock de potion de Force colossale en sommeil profond ? \n"
    "Une entreprise de lutins farceurs cherche à en acheter en grande quantité, je peux faire jouer mes contacts, je connais le DG. »"]

DIMENSIONAL_COMIC =  [
    "🤡 « Monsieur et Madame Hégé ont un fils. Comment ne s'appelle-t-il pas ? Yves ! »",
    "🤡 « Une maman très fière annonce au curé que sa fille a sauté une classe. Le curé répond fièrement : « Moi aussi ! » »",
    "🤡 « Si tu téléphones à une voyante et qu'elle ne décroche pas avant que ça sonne, raccroche ! »",
    "🤡 « Tétraplégique et pakistanais, il invente la marque Tétrapak ! »",
    "🤡 « Le mot « violoncelle » ne doit jamais être suivi des mots « qui court le moins vite ». »",
    "🤡 « C'est l'histoire d'un pingouin qui respire par les fesses. Un jour il s'assied et il meurt. »",
    "🤡 « Les pigeons roux ne vont jamais à la piscine parce que les pigeons roucoulent. »",
    "🤡 « Mon ami est fâché parce qu'il m'a surpris en train de renifler la culotte de sa soeur. Je ne sais pas si c'est parce "
    "\nqu'elle la portait encore, ou que le reste de la famille était présent, mais ça a rendu l'enterrement vraiment difficile. »"]

#------------------------------------------------------ Taxes et emmerdes ----------------------------------------------è---------------------

def taxes_and_fuckeries():

    print("📋 Taxes et emmerdes !")
    print("Sens mon doigt.")

    fuckeries = {
    "Hermine Pingelig, Inspectrice sanitaire de l'ASEPM": random_sanitary_inspection_dialogue,
    "Lucien Cheval, Contrôleur fiscal de la DDDP": random_tax_audit_dialogue
    }

    name, dialogue_function = random.choice(list(fuckeries.items()))
    
    print(f"✨ Vous avez rameuté {CYAN}{name}{RESET} !")
    print()
    start_temporary_event(dialogue_function, "✨ Pfiou... Vous vous demandez s'il vous reste du Transmut-o-Plomb...")


def random_sanitary_inspection_dialogue():
    text = random.choice(SANITARY_INSPECTION)
    return text

def random_tax_audit_dialogue():
    text = random.choice(TAX_AUDIT)
    return text


SANITARY_INSPECTION = [
    "🥼 « Nous avons eu vent de la présence de trois moisissures non déclarées. L'une d'elles affirme être votre comptable. Qu'avez-vous à me dire à ce sujet ? »",
    "🥼 « J'aurais besoin de vérifier la traçabilité de vos mandragores. »",
    "🥼 « Oui tout à fait. Vous pouvez toujours faire une réclamation. Je vous communiquerai la procédure. »",
    "🥼 « Très bien. Je vais contrôler le registre de sécurité... Vous avez bien les 3 copies réglementaires, et la luminescente en cas d'éclipse totale ? »",
    "🥼 « Vous avez bien les containers violets pour les ingrédients bolacés, les containers bleus pour les plantacés et les rouges pour les vivacés n'est-ce pas ? »",
    "🥼 « Mais vous devriez le savoir, c'est la nouvelle législation. »",
    "🥼 « Vous recevrez le compte-rendu sous papyrus dans 15 jours. »",
    "🥼 « L'ASEPM oui... L'Agence de la Salubrité des Établissements de Préparations Magiques. C'est une inspection de routine vous savez. »",
    ] 


TAX_AUDIT = [
    "🏦 « Vous avez déclaré une perte de 300 pièces d'or pour explosion accidentelle. Vous avez les justificatifs ? »",
    "🏦 « Les revenus issus de la transmutation du plomb en or sont imposables, y compris lorsque le plomb appartient aux dents de votre voisin. »",
    "🏦 « Je vais contrôler votre Compta-Grim, c'est par ici ? Ne vous inquiétez pas, ça va bien se passer. Pour moi en tout cas arh arh arh. »",
    "🏦 « C'est étrange, il y a des traces plus claires sur les murs... »",
    "🏦 « Vous avez pensé à remplir le formulaire B-65 ? Sur notre site Inter Maille Élémentaire (ou InterMa comme disent les jeunes) direction_dimensionnelle_deniers_publics.or. »",
    "🏦 « Il y avait un bibelot là. Il y avait un bibelot. Ça se voit à la poussière autour. »",
    "🏦 « Tout a l'air en ordre... J'ai une dernière question avant de partir. »",
    "🏦 « Vous recevrez une copie de mon rapport à la prochaine pleine-lune. »",
    ]

#------------------------------------------------- Explosion pétaradante --------------------------------------------------------------

def crackling_explosion():

    print("💥 Explosion pétaradante !")
    print("Vous essuyez la perte de machin x qtté, truc x qqté, bidule x qqté !")

    # coder la perte des ingrédients avec fonction random :
    # quantité de 1 à 3 ingrédients perdus,
    # 3 ingrédients choisis au hasard dans l'inventaire.

#------------------------------------------------- Transformation de matière --------------------------------------------------------------

def transformation_of_matter(cursor, connection, blending_ingredients):

    print("🦠 Transformation de matière...")

    cursor.execute("""
    SELECT
        ingredients.id,
        ingredients.name,
        rarities.color
    FROM inventory
    JOIN ingredients
        ON ingredients.id = inventory.ingredient_id
    JOIN rarities
        ON rarities.id = ingredients.rarity_id
    """)

    ingredients = cursor.fetchall()
    
    if not ingredients:
        return
    
    number_to_gain = min(len(blending_ingredients), len(ingredients))
    picked_ingredients = random.sample(ingredients, k=number_to_gain)

    for ingredient_id, ingredient_name, ingredient_color in picked_ingredients:

        quantity = random.randint(1, 3)

        add_ingredient_to_inventory(cursor, connection, ingredient_id, quantity)

        print(f"Vous récoltez {COLORS[ingredient_color]}{ingredient_name}{RESET} x{quantity} !")

#------------------------------------------------------ Réaction instable ------------------------------------------------------------------

def surprise_preparation():

    print("🧪 Vous obtenez une préparation impeccable ! Comment ça se fait ? Ca ne vous ressemble pas... ")
    print("   Vous récoltez {item} !")

    # coder l'ajout du produit dans product_inventory, 
    # choix random parmi les produits correspondant à la capacité de l'outil de mélange.


#------------------------------------------------------- Gemino Gemini ---------------------------------------------------------------------

def gemino_gemini(cursor, connection, blending_ingredients):

    print("🧑‍🤝‍🧑 Gemino-Gemini 🎶 Un nous étions, plusieurs nous devenons 🎶 ")

    for ingredient_id in set(blending_ingredients):

        cursor.execute(""" 
            SELECT 
                ingredients.id, 
                ingredients.name, 
                rarities.color 
            FROM ingredients
            JOIN rarities
                ON rarities.id = ingredients.rarity_id
            WHERE ingredients.id = ?
            """, (ingredient_id,))
        

        ingredient = cursor.fetchone()

        if ingredient is None:
            continue

        ingredient_name = ingredient[1]
        ingredient_color = ingredient[2]

        quantity = random.randint(1, 3)
        add_ingredient_to_inventory(cursor, connection, ingredient_id, quantity)
        print(f"Vous récoltez {COLORS[ingredient_color]}{ingredient_name}{RESET} x{quantity} !")






    

    # coder le gain des ingrédients contenus dans blending_ingredients, quantité entre 1 et 3.