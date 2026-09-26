import random

SALE_DIALOGUES = [
    "La jolie guerrière repart ravie, laissant derrière elle les effluves d'un parfum agréable.",
    "Le draeneï glisse quelques pièces sur le comptoir et récupère {item}.",
    "« Je reviendrai ! » promet le voleur en rabattant son capuchon.",
    "L'orc récupère précautionneusement {item} et prend congé avec délicatesse.",
    "Le mort-vivant glisse {item} dans sa sacoche multi-poches avec un rictus satisfait.",
    "La transaction se déroule sans accroc.",
    "Une affaire rondement menée !",
    "Vous gagnez des thunes (ouais) 🎶 Vous êtes à l'aise financièrement... 🎵",
    "Le gnome vous félicite pour l'excellent rapport qualité-prix de {item}.",
    "L'elfe de la nuit repart avec {item} et un grand sourire.",
    "Le chaman, satisfait, range {item} dans sa besace.",
    "Vous emballez soigneusement {item}.",
    "Vous ne vous plaignez pas (non) 🎶 Les affaires marchent en ce moment... 🎵",
    "La vieille voyante vous salue. Affaire conclue !",
    "La clochette tinte tandis que le démoniste s'en va avec un petit signe de la main.",
    "L'ingénieur vous fait un clin d'oeil et disparaît dans un nuage de fumée.",
    "La banshee part en traversant joyeusement la porte en chêne massif.",
    "Une vente de plus ! Les affaires tournent bien.",
    "La prêtresse blanche glisse {item} dans sa robe. « A bientôt... » souffle-t-elle.",
    "Le paladin regarde {item} avec intensité. C'est tout à fait ce dont il avait besoin !",
    "Le chef de guilde est paré pour sa prochaine quête avec {item} !",
    "Le cavalier sans tête met {item} dans son heaume. Au moins il lui a trouvé une utilité...",
    "La goule se frotte les mains. {item} : c'est exactement ce qui lui fallait !",
    "Le druide emporte {item}, soulagé. Il a bien besoin de cet article pour le rassemblement du Corbeau !",
    "Le mage prend son paquet avec empressement.",
    "L'enchanteresse, souriante, récupère son sac de courses : « C'est bien pratique, les commerces de proximité ! »",

]

def random_sale_dialogue(item):
    text = random.choice(SALE_DIALOGUES)
    return text.format(item=item)