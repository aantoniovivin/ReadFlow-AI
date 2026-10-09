import { useEffect, useState } from 'react'
import { BookOpen, GitBranch, Lightbulb, ListChecks } from 'lucide-react'
import { capitalizeSentenceStarts, cleanDocumentText, conciseDocumentHeading, toTitleCase } from '../utils/heading'


const KNOWN_PEOPLE_LIST = [
  'mahatma gandhi', 'gandhi', 'jawaharlal nehru', 'nehru', 'b r ambedkar',
  'ambedkar', 'sardar patel', 'vallabhbhai patel', 'subhas chandra bose', 'bhagat singh',
  'ashoka', 'chandragupta maurya', 'akbar', 'shah jahan', 'aurangzeb',
  'shivaji', 'chhatrapati shivaji', 'abraham lincoln', 'lincoln', 'george washington',
  'washington', 'napoleon bonaparte', 'napoleon', 'julius caesar', 'caesar',
  'alexander the great', 'cleopatra', 'nelson mandela', 'mandela', 'martin luther king',
  'martin luther king jr', 'winston churchill', 'churchill', 'franklin d roosevelt', 'roosevelt',
  'karl marx', 'marx', 'adam smith', 'john locke', 'voltaire',
  'rousseau', 'plato', 'socrates'
]

const KNOWN_SCIENTISTS_LIST = [
  'albert einstein', 'isaac newton', 'charles darwin', 'darwin', 'gregor mendel', 'mendel', 'marie curie',
  'galileo galilei', 'galileo', 'dmitri mendeleev', 'mendeleev', 'louis pasteur', 'pasteur', 'rosalind franklin',
  'james watson', 'watson', 'francis crick', 'crick', 'watson and crick', 'carl linnaeus', 'carolus linnaeus',
  'linnaeus', 'linn.', 'linn', 'aristotle', 'robert hooke', 'antonie van leeuwenhoek', 'leeuwenhoek',
  'alexander fleming', 'fleming', 'nikola tesla', 'michael faraday', 'max planck', 'niels bohr',
  'johannes kepler', 'edwin hubble', 'ada lovelace', 'alan turing', 'srinivasa ramanujan', 'c v raman',
  'chandrasekhara venkata raman', 'j c bose', 'jagadish chandra bose', 'a p j abdul kalam', 'abdul kalam',
  'ernst mayr', 'mayr', 'jean-baptiste lamarck', 'lamarck', 'r h whittaker', 'whittaker', 'ernst haeckel',
  'haeckel', 'theophrastus', 'john ray', 'george bentham', 'bentham', 'joseph dalton hooker', 'hooker',
  'bentham and hooker', 'carl woese', 'woese', 'theodor schwann', 'schwann', 'matthias schleiden', 'schleiden',
  'rudolf virchow', 'virchow', 'camillo golgi', 'golgi', 'christian de duve', 'de duve', 'george palade',
  'palade', 'melvin calvin', 'calvin', 'hans krebs', 'krebs', 'thomas hunt morgan', 't h morgan', 'morgan',
  'alfred sturtevant', 'sturtevant', 'henking', 'francois jacob', 'jacques monod', 'jacob and monod',
  'frederick griffith', 'griffith', 'oswald avery', 'avery', 'colin macleod', 'macleod', 'maclyn mccarty',
  'mccarty', 'alfred hershey', 'hershey', 'martha chase', 'chase', 'hershey and chase', 'matthew meselson',
  'meselson', 'franklin stahl', 'stahl', 'meselson and stahl', 'har gobind khorana', 'khorana',
  'marshall nirenberg', 'nirenberg', 'severo ochoa', 'ochoa', 'alec jeffreys', 'jeffreys', 'kary mullis',
  'mullis', 'norman borlaug', 'borlaug', 'm s swaminathan', 'swaminathan', 'panchanan maheshwari', 'maheshwari',
  'ramdeo misra', 'edward o wilson', 'e o wilson', 'alexander von humboldt', 'humboldt', 'robert may',
  'paul ehrlich', 'ehrlich', 'karl landsteiner', 'landsteiner', 'william bateson', 'bateson', 'reginald punnett',
  'punnett', 'hugo de vries', 'de vries', 'carl correns', 'correns', 'erich von tschermak', 'tschermak',
  'walter sutton', 'sutton', 'theodor boveri', 'boveri', 'sutton and boveri', 'george beadle', 'beadle',
  'edward tatum', 'tatum', 'archibald garrod', 'garrod', 'jane goodall', 'dian fossey', 'stephen hawking',
  'richard feynman', 'thomas edison', 'william harvey', 'edward jenner', 'jonas salk', 'barbara mcclintock',
  'dorothy hodgkin', 'emmy noether', 'katherine johnson', 'mary anning'
]

const KNOWN_LOCATIONS_LIST = [
  'afghanistan', 'africa', 'albania', 'algeria', 'alps', 'amazon',
  'amazon rainforest', 'amazon river', 'america', 'andes', 'andhra pradesh', 'andorra',
  'angola', 'antarctica', 'antigua and barbuda', 'arctic ocean', 'argentina', 'armenia',
  'arunachal pradesh', 'asia', 'assam', 'atlantic ocean', 'australia', 'austria',
  'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus',
  'belgium', 'belize', 'benin', 'bhutan', 'bihar', 'bolivia',
  'bosnia and herzegovina', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina faso',
  'burundi', 'california', 'cambodia', 'cameroon', 'canada', 'cape verde',
  'central african republic', 'chad', 'chhattisgarh', 'chile', 'china', 'colombia',
  'comoros', 'congo', 'costa rica', 'croatia', 'cuba', 'cyprus',
  'czech republic', 'czechia', 'delhi', 'denmark', 'djibouti', 'dominica',
  'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea',
  'estonia', 'eswatini', 'ethiopia', 'europe', 'fiji', 'finland',
  'florida', 'france', 'gabon', 'gambia', 'ganga', 'ganga river',
  'georgia', 'germany', 'ghana', 'goa', 'greece', 'grenada',
  'guatemala', 'guinea', 'guinea-bissau', 'gujarat', 'guyana', 'haiti',
  'haryana', 'himachal pradesh', 'himalayas', 'honduras', 'hungary', 'iceland',
  'illinois', 'india', 'indian ocean', 'indonesia', 'iran', 'iraq',
  'ireland', 'israel', 'italy', 'ivory coast', 'jamaica', 'jammu and kashmir',
  'japan', 'jharkhand', 'jordan', 'karnataka', 'kazakhstan', 'kenya',
  'kerala', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan', 'ladakh',
  'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya',
  'liechtenstein', 'lithuania', 'luxembourg', 'madagascar', 'madhya pradesh', 'maharashtra',
  'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'manipur',
  'marshall islands', 'mauritania', 'mauritius', 'meghalaya', 'mexico', 'micronesia',
  'mizoram', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco',
  'mozambique', 'myanmar', 'nagaland', 'namibia', 'nauru', 'nepal',
  'netherlands', 'new york', 'new zealand', 'nicaragua', 'niger', 'nigeria',
  'nile', 'nile river', 'north america', 'north carolina', 'north korea', 'north macedonia',
  'norway', 'oceania', 'odisha', 'ohio', 'oman', 'pacific ocean',
  'pakistan', 'palau', 'palestine', 'panama', 'papua new guinea', 'paraguay',
  'pennsylvania', 'peru', 'philippines', 'poland', 'portugal', 'punjab',
  'qatar', 'rajasthan', 'rio', 'rio de janeiro', 'romania', 'russia',
  'rwanda', 'sahara', 'sahara desert', 'saint kitts and nevis', 'saint lucia', 'saint vincent and the grenadines',
  'samoa', 'san marino', 'saudi arabia', 'senegal', 'serbia', 'seychelles',
  'sierra leone', 'sikkim', 'singapore', 'slovakia', 'slovenia', 'solomon islands',
  'somalia', 'south africa', 'south america', 'south korea', 'south sudan', 'southern ocean',
  'spain', 'sri lanka', 'sudan', 'suriname', 'sweden', 'switzerland',
  'syria', 'taiwan', 'tajikistan', 'tamil nadu', 'tanzania', 'telangana',
  'texas', 'thailand', 'timor-leste', 'togo', 'tonga', 'trinidad and tobago',
  'tripura', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda',
  'uk', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'uruguay',
  'usa', 'uttar pradesh', 'uttarakhand', 'uzbekistan', 'vanuatu', 'vatican city',
  'venezuela', 'vietnam', 'washington', 'west bengal', 'western ghats', 'yemen',
  'zambia', 'zimbabwe'
]

const GENERIC_STOPWORDS_FILTER = new Set([
  'a', 'about', 'above', 'absence', 'across', 'after',
  'afterwards', 'again', 'against', 'all', 'almost', 'alone',
  'along', 'already', 'also', 'although', 'always', 'am',
  'among', 'amongst', 'amount', 'an', 'and', 'another',
  'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere',
  'appears after', 'are', 'are included', 'are included in', 'around',
  'as', 'asset', 'at', 'at the end of', 'author', 'availability',
  'back', 'based', 'based on', 'based on the', 'be', 'became',
  'because', 'become', 'becomes', 'becoming', 'been', 'before',
  'beforehand', 'behind', 'being', 'belong to', 'below', 'beside',
  'besides', 'best', 'between', 'beyond', 'bodies', 'body',
  'both', 'bottom', 'but', 'by', 'call', 'called',
  'can', 'cannot', 'cant', 'capital letter',
  'certain', 'character',
  'common', 'common features',
  'complex', 'condition', 'conditions', 'core', 'could', 'couldnt',
  'deep', 'defined', 'describe', 'described', 'described but',
  'described by', 'detail', 'development', 'difference', 'differences', 'different',
  'distinct', 'do', 'does', 'done', 'double',
  'down', 'due', 'during', 'each', 'early', 'early attempts',
  'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere',
  'empty', 'endogenously', 'enough', 'etc', 'even', 'ever',
  'every', 'everyone', 'everything', 'everywhere', 'example', 'examples',
  'except', 'exogenously', 'factor', 'factors', 'false', 'feature',
  'features', 'feet', 'few', 'fifteen', 'fifty', 'find',
  'finite', 'first', 'first word', 'five', 'following', 'for',
  'for human being', 'for human beings', 'form', 'former', 'formerly', 'forms',
  'forty', 'found', 'free', 'from', 'front',
  'full', 'further', 'get', 'give', 'given', 'gives',
  'go', 'goes', 'gone', 'good', 'great', 'greater',
  'group', 'groups', 'had', 'has', 'hasnt', 'have',
  'he', 'help', 'helps', 'hence', 'her', 'here',
  'hers', 'herself', 'high', 'him', 'himself',
  'his', 'his publication', 'how', 'however', 'human being', 'human beings',
  'hundred', 'i', 'identified and', 'ie', 'if',
  'important', 'impossible', 'in', 'include', 'includes', 'including',
  'indeed', 'indicates that', 'influence', 'influences', 'into', 'is',
  'is included', 'is written in', 'is written in an', 'it', 'its', 'itself',
  'just', 'keep', 'known', 'large', 'large number', 'last',
  'late', 'latter', 'least', 'less',
  'level', 'levels', 'lifestyle', 'like', 'line', 'lines',
  'living', 'living things', 'living world', 'long',
  'low', 'made', 'magnitude', 'main', 'major', 'make',
  'makes', 'many', 'may', 'me',
  'means', 'meanwhile', 'member', 'members', 'might', 'minor',
  'more', 'moreover', 'most', 'mostly',
  'move', 'much', 'must', 'my', 'myself', 'name',
  'namely', 'nearly', 'nearly impossible', 'need', 'needs', 'neither',
  'never', 'nevertheless', 'next', 'nine', 'no', 'nobody',
  'none', 'noone', 'nor', 'not', 'nothing',
  'now', 'nowhere', 'number', 'numbers', 'of', 'off',
  'often', 'on', 'once', 'one', 'only', 'onto',
  'or', 'other', 'others', 'otherwise',
  'our', 'ours', 'ourselves', 'out', 'over', 'own',
  'part', 'parts', 'per', 'perhaps', 'planning',
  'please', 'point', 'points', 'presence', 'presence of',
  'present', 'presents', 'produce', 'produced',
  'producing', 'proportion', 'publication', 'put', 'putting', 'quantity',
  'rather', 'refers', 'region', 'regions', 'resource', 'resources',
  'sac', 'same', 'see', 'seem', 'seemed', 'seeming',
  'seems', 'segment', 'several', 'she', 'short', 'should',
  'show', 'shown', 'shows', 'side', 'similar', 'simple',
  'simple morphology', 'since', 'single', 'singular', 'six', 'small',
  'small letter', 'so', 'society', 'some', 'somehow', 'someone',
  'something', 'sometime', 'sometimes', 'somewhere', 'special', 'stage',
  'stages', 'starts with', 'state', 'states', 'still', 'still remains',
  'such',
  'take', 'taken', 'takes', 'term', 'terms', 'terms of',
  'than', 'that', 'the', 'the author', 'the biological name', 'the biological name and',
  'the example of', 'the living', 'the living world', 'the specific', 'the specific epithet', 'their',
  'them', 'themselves', 'then', 'there', 'therefore', 'these',
  'they', 'third', 'this', 'this species', 'those', 'though',
  'three', 'through', 'throughout', 'thus', 'title', 'to',
  'to study', 'to study all', 'together', 'too', 'top', 'toward',
  'towards', 'two', 'type', 'types', 'under', 'until',
  'up', 'upon', 'us', 'used systema',
  'very', 'very range', 'via', 'was',
  'was first', 'was first described', 'we', 'well', 'were', 'what',
  'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
  'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether',
  'which', 'while', 'who', 'whoever', 'whole', 'whom',
  'whose', 'why', 'wide', 'will', 'with', 'within',
  'without', 'word', 'words', 'work', 'works', 'would',
  'written these', 'yet', 'you', 'your', 'yours', 'yourself'
])

const INVALID_CONNECTOR_WORDS = new Set([
  'a', 'an', 'the', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'about', 'into', 'to', 'from', 'up', 'down',
  'off', 'over', 'under', 'as', 'this', 'that', 'these', 'those', 'which', 'what', 'where', 'when', 'how', 'who',
  'whom', 'whose', 'why', 'and', 'or', 'but', 'if', 'because', 'while', 'though', 'although', 'is', 'are', 'was',
  'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'used', 'based', 'starts', 'include',
  'includes', 'including', 'included', 'belong', 'belongs', 'described', 'appears', 'written', 'denoting', 'contains',
  'consists', 'refers', 'defined', 'indicated', 'indicates', 'shows', 'shown', 'found', 'gives', 'given', 'so',
  'such', 'very', 'nearly', 'almost', 'also', 'all', 'any', 'some', 'many', 'each', 'few', 'more', 'most', 'not',
  'nor', 'only', 'first', 'last', 'his', 'her', 'their', 'its', 'my', 'your', 'our', 'he', 'she', 'it', 'they', 'we', 'you', 'i'
])

const INVALID_VERB_AND_ACTION_WORDS = new Set([
  'include', 'includes', 'included', 'including', 'write', 'writes', 'written', 'writing',
  'describe', 'describes', 'described', 'describing', 'indicate', 'indicates', 'indicated', 'indicating',
  'appear', 'appears', 'appeared', 'appearing', 'remain', 'remains', 'remained', 'remaining',
  'belong', 'belongs', 'belonged', 'belonging', 'study', 'studies', 'studied', 'studying',
  'identify', 'identifies', 'identified', 'identifying', 'show', 'shows', 'shown', 'showing',
  'make', 'makes', 'made', 'making', 'take', 'takes', 'taken', 'taking',
  'give', 'gives', 'given', 'giving', 'find', 'finds', 'found', 'finding',
  'call', 'called', 'calling', 'use', 'used', 'using', 'state', 'states', 'stated', 'stating',
  'provide', 'provides', 'provided', 'providing', 'consist', 'consists', 'consisted', 'consisting',
  'denote', 'denotes', 'denoted', 'denoting', 'enlarge', 'enlarges', 'enlarged', 'enlarging',
  'illustrate', 'illustrates', 'illustrated', 'illustrating', 'contain', 'contains', 'contained',
  'group', 'grouped', 'grouping', 'relate', 'related', 'relating', 'divide', 'divided', 'dividing'
])

const CORE_SCIENCE_LIST = [
  'couplet', 'lead', 'leads', 'monograph', 'monographs', 'manual', 'manuals',
  'catalogue', 'catalogues', 'classification', 'taxonomic categories', 'taxonomic hierarchy',
  'hierarchy', 'taxa', 'taxon', 'biodiversity', 'diversity', 'identification', 'nomenclature',
  'binomial nomenclature', 'binomial', 'systema naturae', 'species plantarum',
  'carolus linnaeus', 'linnaeus', 'ernst mayr', 'mayr',
  'homo sapiens', 'homo', 'sapiens', 'mangifera indica', 'mangifera', 'solanum tuberosum', 'solanum',
  'panthera leo', 'panthera tigris', 'panthera pardus', 'panthera', 'felis catus', 'felis',
  'canis lupus', 'canis', 'musca domestica', 'musca', 'triticum aestivum', 'triticum',
  'hominidae', 'muscidae', 'anacardiaceae', 'solanaceae', 'poaceae', 'felidae', 'canidae',
  'primata', 'diptera', 'sapindales', 'polemoniales', 'poales', 'carnivora',
  'mammalia', 'insecta', 'dicotyledonae', 'monocotyledonae',
  'chordata', 'arthropoda', 'angiospermae', 'gymnospermae',
  'notochord', 'dorsal hollow nerve cord', 'pharyngeal gill slits',
  'herbarium', 'botanical garden', 'botanical gardens', 'museum', 'zoological park', 'zoological parks',
  'flora', 'fauna', 'icbn', 'iczn', 'taxonomic key', 'keys', 'key',
  'order', 'orders', 'family', 'families', 'genus', 'genera', 'species', 'kingdom', 'kingdoms', 'phylum', 'division',

  '1nf', '2nf', '3-phosphoglycerate', '3nf', '5\' cap', 'a* search algorithm',
  'aba', 'abscisic acid', 'absorption', 'abstract class', 'abstract classes', 'abstract factory pattern',
  'abstraction', 'ac', 'acceleration', 'acceleration due to gravity', 'accumulator', 'acetaldehyde',
  'acetic acid', 'acetone', 'acetophenone', 'acetylcholine', 'acetylene', 'acid',
  'acid anhydride', 'acid dissociation constant', 'acid properties', 'acidic oxide', 'acids', 'actin',
  'actinides', 'actinoids', 'action potential', 'action-reaction', 'activation energy', 'activation function',
  'active immunity', 'active site', 'acyl chloride', 'adam optimizer', 'adaptation', 'adapter pattern',
  'adaptive immunity', 'adaptive radiation', 'addition polymerization', 'address bus', 'address resolution protocol', 'adenine',
  'adh', 'adiabatic process', 'adjacency list', 'adjacency matrix', 'adrenal cortex', 'adrenal gland',
  'adrenal medulla', 'adrenaline', 'advanced encryption standard', 'adventitious root', 'adware', 'aerobic respiration',
  'aes', 'afforestation', 'agar', 'agaricus', 'agenda 21', 'agile',
  'agile methodology', 'agranulocyte', 'ai', 'albugo', 'alcohol', 'alcohols',
  'aldehyde', 'aldehydes', 'aldol condensation', 'aldosterone', 'algae', 'algorithm',
  'algorithms', 'alimentary canal', 'alkali metals', 'alkaline earth metals', 'alkane', 'alkanes',
  'alkene', 'alkenes', 'alkyl halide', 'alkyne', 'alkynes', 'allele',
  'alleles', 'allergens', 'allergy', 'alpha decay', 'alpha helix', 'alternating current',
  'alternative hypothesis', 'alternative splicing', 'altruism', 'alu', 'alveoli', 'alveolus',
  'american revolution', 'amide', 'amides', 'amine', 'amines', 'amino acid',
  'amino acids', 'aminoacyl-trna', 'aminoacyl-trna synthetase', 'ammeter', 'ammonia', 'ammonotelic',
  'amniotic fluid', 'amniotic sac', 'amoeba', 'amortized analysis', 'ampere', 'ampere\'s circuital law',
  'amphibia', 'amphibian', 'amphibians', 'amphoteric oxide', 'amplitude', 'amygdala',
  'amylopectin', 'amylose', 'anabolism', 'anaerobic respiration', 'analogous organs', 'analyte',
  'anaphylaxis', 'anatomy', 'ancient egypt', 'ancient greece', 'and gate', 'androecium',
  'androgen', 'androgens', 'andromeda', 'anemophily', 'aneuploidy', 'anf',
  'angiosperm', 'angiospermae', 'angiosperms', 'angiotensin', 'angle of contact', 'angular',
  'angular acceleration', 'angular displacement', 'angular momentum', 'angular velocity', 'aniline', 'animalia',
  'anion', 'anions', 'ann', 'annelida', 'annelids', 'annual ring',
  'annual rings', 'anode', 'ans', 'anterior pituitary', 'anther', 'anthers',
  'anthracene', 'anti-markovnikov rule', 'antibodies', 'antibody', 'antibonding orbital', 'anticodon',
  'anticodons', 'anticyclone', 'antidiuretic hormone', 'antigen', 'antigens', 'antinode',
  'antinodes', 'antiparallel', 'anus', 'aorta', 'apache kafka', 'apfs',
  'api', 'apical bud', 'apis', 'appendicular skeleton', 'appendix', 'application layer',
  'aquifer', 'arachnida', 'arachnids', 'arachnoid mater', 'archaea', 'archimedes\' principle',
  'arene', 'arenes', 'arithmetic logic unit', 'arm architecture', 'aromatic hydrocarbon', 'aromaticity',
  'arp', 'array', 'arrays', 'arrhenius acid', 'arrhenius base', 'arrhenius equation',
  'arteries', 'artery', 'arthropoda', 'arthropods', 'artificial intelligence', 'artificial neural network',
  'ascaris', 'asci', 'ascomycetes', 'ascospores', 'ascus', 'asexual reproduction',
  'aspergillus', 'assembly', 'assembly language', 'assimilation', 'associative array', 'asteroid',
  'asteroid belt', 'asteroids', 'asthenosphere', 'astronomical telescope', 'astronomy', 'asymmetric encryption',
  'asymmetric-key cryptography', 'asymptotic analysis', 'async/await', 'atmosphere', 'atmospheric pressure', 'atom',
  'atomic mass', 'atomic nucleus', 'atomic number', 'atomic radius', 'atomicity', 'atoms',
  'atrial natriuretic factor', 'atrioventricular node', 'atrium', 'attention mechanism', 'auditory canal', 'aufbau principle',
  'aurelia', 'authentication', 'authorization', 'autoimmune disease', 'autoionization of water', 'automata theory',
  'autonomic nervous system', 'autosome', 'autosomes', 'auxin', 'auxins', 'average velocity',
  'aves', 'avl tree', 'avl trees', 'avogadro constant', 'avogadro\'s law', 'avogadro\'s number',
  'aws', 'axial skeleton', 'axillary bud', 'axon', 'axons', 'azimuthal quantum number',
  'azure', 'b cell', 'b lymphocyte', 'b+ tree', 'b+ trees', 'b-tree',
  'b-tree index', 'b-trees', 'backend', 'backpropagation', 'backtracking', 'bacteria',
  'bacteriophage', 'bakelite', 'ball and socket joint', 'balmer series', 'bandwidth', 'banker\'s algorithm',
  'bar magnet', 'bark', 'barrier potential', 'basalt', 'base', 'base dissociation constant',
  'base pair', 'base pairs', 'bases', 'bash', 'basic oxide', 'basidia',
  'basidiomycetes', 'basidiospores', 'basidium', 'basophil', 'basophils', 'batch normalization',
  'batch size', 'battery', 'bcnf', 'bdd', 'beats', 'behavior-driven development',
  'bellman-ford', 'bellman-ford algorithm', 'benzaldehyde', 'benzene', 'benzoic acid', 'bernoulli\'s equation',
  'bernoulli\'s principle', 'bert', 'beta decay', 'beta sheet', 'bfs', 'bgp',
  'bias-variance tradeoff', 'bicarbonate', 'bidentate ligand', 'big bang', 'big bang theory', 'big o notation',
  'bile', 'bile pigments', 'bile salts', 'bilirubin', 'biliverdin', 'binary',
  'binary fission', 'binary heap', 'binary indexed tree', 'binary search', 'binary search tree', 'binary tree',
  'binary trees', 'binding energy', 'binding energy per nucleon', 'binomial nomenclature', 'biodiversity', 'biomass',
  'biome', 'biomes', 'bios', 'biosphere', 'biosphere reserve', 'biot-savart law',
  'bipartite graph', 'birds', 'bit manipulation', 'bitcoin', 'bitmap index', 'bivalvia',
  'black hole', 'blackbody', 'blackbody radiation', 'blast furnace', 'blastocyst', 'blastomere',
  'blastula', 'blind spot', 'blockchain', 'blood', 'blood pressure', 'bloom filter',
  'blotting', 'bluetooth', 'bohr model', 'boiling point', 'boiling point elevation', 'bond energy',
  'bond length', 'bond order', 'bonding orbital', 'bone', 'bone marrow', 'bones',
  'boolean', 'booleans', 'border gateway protocol', 'bose-einstein condensate', 'boson', 'bosons',
  'botanical garden', 'botanical gardens', 'botany', 'botnet', 'botnets', 'bottleneck effect',
  'bowman\'s capsule', 'boyce-codd normal form', 'boyer-moore algorithm', 'boyle\'s law', 'brackett series', 'brain',
  'branch', 'branch and bound', 'branch prediction', 'breadth-first search', 'brewster\'s law', 'bronchi',
  'bronchiole', 'bronchioles', 'bronchus', 'bronsted-lowry acid', 'bronsted-lowry base', 'brown algae',
  'browser', 'bryophyta', 'bryophyte', 'bryophytes', 'bst', 'btrfs',
  'bubble sort', 'bucket sort', 'bud', 'budding', 'buffer overflow', 'buffer overflow attack',
  'buffer solution', 'builder pattern', 'bundle of his', 'buoyancy', 'buoyant force', 'bus',
  'butane', 'butanol', 'butene', 'butyne', 'bytecode', 'byzantine fault tolerance',
  'c language', 'c#', 'c++', 'c3 cycle', 'c3 plants', 'c4 cycle',
  'c4 pathway', 'c4 plants', 'ca', 'cache', 'cache coherency', 'cache memory',
  'caecum', 'calcination', 'calcitonin', 'calculus', 'callback', 'callbacks',
  'calorimeter', 'calorimetry', 'calvin cycle', 'calyx', 'cam pathway', 'cam plants',
  'cambium', 'candidate key', 'canine', 'cannizzaro reaction', 'cap theorem', 'capacitance',
  'capacitive reactance', 'capacitor', 'capacitors', 'capillaries', 'capillarity', 'capillary',
  'capillary rise', 'capitalism', 'carbaminohemoglobin', 'carbanion', 'carbocation', 'carbohydrate',
  'carbohydrates', 'carbon cycle', 'carbon dating', 'carbon dioxide transport', 'carbon tetrachloride', 'carbonate',
  'carboxylic acid', 'carboxylic acids', 'cardiac cycle', 'cardiac muscle', 'carnivore', 'carnivores',
  'carnot cycle', 'carnot engine', 'carotenoid', 'carotenoids', 'carpel', 'carpels',
  'carrying capacity', 'cartilage', 'cas9', 'casparian strip', 'cassandra', 'catabolism',
  'catalysis', 'catalyst', 'catalysts', 'cathode', 'cation', 'cations',
  'cdn', 'cecum', 'cell body', 'cellular organization', 'cellular respiration', 'cellulose',
  'center of mass', 'central limit theorem', 'central nervous system', 'central processing unit', 'centrifugal force', 'centripetal acceleration',
  'centripetal force', 'cephalopoda', 'cerebellum', 'cerebral cortex', 'cerebral hemisphere', 'cerebrospinal fluid',
  'cerebrum', 'certificate authority', 'chain reaction', 'charles\'s law', 'chelate', 'chelating agent',
  'chemical bond', 'chemical bonding', 'chemical equilibrium', 'chemical kinetics', 'chemistry', 'chiasma',
  'chipset', 'chiral center', 'chirality', 'chlamydomonas', 'chloroform', 'chlorophyceae',
  'chlorophyll', 'chlorophyll a', 'chlorophyll b', 'chloroplast', 'chloroplasts', 'chola dynasty',
  'cholesterol', 'chondrichthyes', 'chondrocyte', 'chordata', 'chordates', 'chromosome',
  'chromosomes', 'chrysophytes', 'chyme', 'chymotrypsin', 'ci/cd', 'cidr notation',
  'ciliates', 'ciphertext', 'circadian rhythm', 'circuit switching', 'circular linked list', 'circular motion',
  'cis-trans isomerism', 'cisc', 'civil disobedience movement', 'civilization', 'civilizations', 'cladistics',
  'cladogram', 'class', 'classes', 'clean architecture', 'cleavage', 'clemmensen reduction',
  'cli', 'client', 'climate change', 'cloning vector', 'closed system', 'closure',
  'closures', 'clotting', 'cloud computing', 'cnidaria', 'cnidarians', 'cnn',
  'cns', 'coagulation', 'coal', 'cochlea', 'code refactoring', 'codominance',
  'codon', 'codons', 'coefficient of friction', 'coefficient of viscosity', 'coelenterata', 'coherent sources',
  'cohesion-tension theory', 'cold war', 'collecting duct', 'colligative properties', 'collision resolution', 'collision theory',
  'colon', 'colonialism', 'colostrum', 'columnar database', 'combination', 'comet',
  'comets', 'command pattern', 'commensalism', 'commit', 'common ion effect', 'compact bone',
  'companion cell', 'companion cells', 'competition', 'compiled language', 'compiler', 'compilers',
  'complex ion', 'composite key', 'compound', 'compound leaf', 'compound microscope', 'compounds',
  'computer network', 'computer networks', 'computer virus', 'computer vision', 'computer worm', 'concave lens',
  'concave mirror', 'concurrency', 'concurrency control', 'condensation', 'condensation polymerization', 'conditional statement',
  'conditioning', 'conduction', 'conductivity', 'conductor', 'cones', 'confidence interval',
  'conformation', 'conidia', 'conidiophore', 'conidiophores', 'conifer', 'conifers',
  'conjugate acid', 'conjugate base', 'consciousness', 'consensus algorithm', 'consensus mechanism', 'conservation',
  'conservation of angular momentum', 'conservation of energy', 'conservation of momentum', 'conservative force', 'consistency', 'constant',
  'constants', 'constellation', 'constitution', 'constructive interference', 'constructor', 'constructors',
  'consumer', 'consumers', 'container', 'containerization', 'containers', 'content delivery network',
  'context switch', 'context switching', 'context-free grammar', 'continental drift', 'continuity', 'continuous deployment',
  'continuous integration', 'control bus', 'control unit', 'convection', 'convergent evolution', 'convex lens',
  'convex mirror', 'convolutional neural network', 'coordinate bond', 'coordination compound', 'coordination compounds', 'coordination number',
  'corals', 'coriolis effect', 'cork', 'cork cambium', 'cornea', 'corolla',
  'coronary artery', 'coroutine', 'coroutines', 'corpus callosum', 'correlation', 'corrosion',
  'cortex', 'corticosteroids', 'cortisol', 'cosmic microwave background', 'cotyledon', 'cotyledons',
  'couchdb', 'coulomb\'s law', 'counting sort', 'courtship', 'covalent bond', 'covalent bonding',
  'covalent bonds', 'cpu', 'crispr', 'crispr-cas9', 'critical angle', 'critical pressure',
  'critical section', 'critical temperature', 'cross product', 'cross-bridge cycle', 'cross-entropy loss', 'cross-pollination',
  'cross-site request forgery', 'cross-site scripting', 'crossing over', 'crust', 'crustacea', 'crustaceans',
  'cryptanalysis', 'cryptocurrency', 'cryptographic hash function', 'cryptography', 'crystal field splitting', 'crystal field theory',
  'csf', 'csrf', 'css', 'cubical expansion', 'current density', 'current electricity',
  'currying', 'cuticle', 'cybersecurity', 'cycas', 'cycloalkane', 'cycloalkanes',
  'cyclohexane', 'cyclone', 'cytokinin', 'cytokinins', 'cyton', 'cytosine',
  'cytotoxic t cell', 'd orbital', 'dacron', 'dag', 'dalton\'s law', 'damped oscillation',
  'dandi march', 'dangling pointer', 'dark energy', 'dark matter', 'data bus', 'data encryption standard',
  'data lake', 'data link layer', 'data mart', 'data structure', 'data structures', 'data type',
  'data types', 'data warehouse', 'database', 'database index', 'database management system', 'database normalization',
  'database replication', 'database schema', 'database sharding', 'database transaction', 'database transactions', 'databases',
  'dative bond', 'davisson-germer experiment', 'dbms', 'dc', 'dct', 'ddos',
  'ddos attack', 'ddr4', 'ddr5', 'de broglie hypothesis', 'de broglie wavelength', 'deadlock',
  'deadlocks', 'debugging', 'decane', 'decentralized finance', 'decision tree', 'decision trees',
  'declaration of independence', 'declarative programming', 'decoder', 'decomposer', 'decomposers', 'decorator pattern',
  'decryption', 'deep learning', 'defecation', 'defi', 'definite integral', 'deforestation',
  'deletion', 'delhi sultanate', 'democracy', 'demultiplexer', 'denaturation', 'dendrite',
  'dendrites', 'denial of service', 'denial-of-service attack', 'density', 'depletion region', 'depolarization',
  'deposition', 'depth-first search', 'deque', 'derivative', 'derivatives', 'des',
  'desertification', 'design pattern', 'design patterns', 'destructive interference', 'destructor', 'destructors',
  'determinant', 'determinants', 'detritivore', 'detritivores', 'deuteromycetes', 'device driver',
  'device drivers', 'devops', 'dfs', 'dhcp', 'diamagnetism', 'diaphragm',
  'diastereomer', 'diastereomers', 'diastole', 'dicots', 'dicotyledonae', 'dictyota',
  'dielectric', 'dielectric constant', 'diethyl ether', 'differentiability', 'differential calculus', 'differential equation',
  'differential equations', 'diffie-hellman key exchange', 'diffraction', 'diffusion', 'diffusion model', 'diffusion models',
  'digestion', 'digestive tract', 'digital certificate', 'digital certificates', 'digital signature', 'digital signatures',
  'dihybrid cross', 'dijkstra', 'dijkstra\'s algorithm', 'dimensionality reduction', 'dinoflagellates', 'dioptre',
  'dipole moment', 'dipole-dipole interaction', 'direct current', 'direct memory access', 'directed acyclic graph', 'directed graph',
  'disaccharide', 'disaccharides', 'disjoint set', 'disjoint-set data structure', 'dispersion', 'displacement',
  'displacement current', 'distal convoluted tubule', 'distance', 'distributed denial-of-service attack', 'distributed hash table', 'distributed ledger technology',
  'distributed system', 'distributed systems', 'divergent evolution', 'divide and conquer', 'divide-and-conquer algorithm', 'division',
  'django', 'dma', 'dna', 'dna cloning', 'dna fingerprinting', 'dna ligase',
  'dna methylation', 'dna microarray', 'dna polymerase', 'dna primase', 'dna replication', 'dns',
  'docker', 'domain name system', 'dominant allele', 'dopamine', 'doping', 'doppler effect',
  'dorsal hollow neural system', 'dos', 'dos attack', 'dot product', 'double fertilization', 'double helix',
  'double-ended queue', 'doubly linked list', 'down syndrome', 'dram', 'drift velocity', 'dropout',
  'dry principle', 'dual nature of matter', 'duck typing', 'duodenum', 'duplication', 'dura mater',
  'durability', 'dwarf planet', 'dynamic array', 'dynamic equilibrium', 'dynamic host configuration protocol', 'dynamic programming',
  'dynamic typing', 'dynamics', 'dynamodb', 'e1 reaction', 'e2 reaction', 'e2e testing',
  'ear', 'eardrum', 'earth', 'earth summit', 'earth\'s magnetic field', 'earthquake',
  'earthquakes', 'earthworm', 'ecc', 'ecg', 'echinodermata', 'echinoderms',
  'ecological niche', 'ecological pyramid', 'ecology', 'ecosystem', 'ecosystems', 'ectoderm',
  'eddy currents', 'edta', 'eeprom', 'effective nuclear charge', 'egestion', 'egg cell',
  'eigenvalue', 'eigenvalues', 'eigenvector', 'eigenvectors', 'einstein\'s photoelectric equation', 'elastic potential energy',
  'electric charge', 'electric current', 'electric field', 'electric field intensity', 'electric field lines', 'electric flux',
  'electric potential', 'electric power', 'electrocardiogram', 'electrochemical cell', 'electrochemistry', 'electrolysis',
  'electrolytic cell', 'electromagnetic induction', 'electromagnetic spectrum', 'electromagnetic wave', 'electromagnetism', 'electromeric effect',
  'electromotive force', 'electron', 'electron affinity', 'electron configuration', 'electronegativity', 'electrons',
  'electrophile', 'electrophilic aromatic substitution', 'electrostatic potential energy', 'electrostatics', 'element', 'elements',
  'elisa', 'elliptic-curve cryptography', 'embryo', 'embryo sac', 'emf', 'empirical formula',
  'enantiomer', 'enantiomers', 'encapsulation', 'encoder', 'encryption', 'end point',
  'end-to-end testing', 'endangered species', 'endemic species', 'endocarp', 'endocrine gland', 'endocrine glands',
  'endocrine system', 'endoderm', 'endodermis', 'endoskeleton', 'endosperm', 'endothermic',
  'endothermic reaction', 'energy', 'enlightenment', 'enthalpy', 'entomophily', 'entropy',
  'enzyme', 'enzymes', 'eosinophil', 'eosinophils', 'epicarp', 'epicenter',
  'epidermis', 'epigenetics', 'epiglottis', 'epinephrine', 'epistasis', 'epoch',
  'epochs', 'eprom', 'equation of continuity', 'equator', 'equilibrium constant', 'equipotential surface',
  'equivalence point', 'erosion', 'erythrocyte', 'erythrocytes', 'escape velocity', 'esophagus',
  'essential amino acids', 'ester', 'esterification', 'esters', 'estivation', 'estrogen',
  'ethane', 'ethanol', 'ethene', 'ether', 'ethereum', 'ethernet',
  'ethers', 'ethical hacking', 'ethology', 'ethyl acetate', 'ethylene', 'ethyne',
  'etl', 'euglena', 'euglenoids', 'eukaryote', 'eukaryotes', 'eustachian tube',
  'evaporation', 'event horizon', 'event loop', 'eventual consistency', 'evolution', 'ex situ conservation',
  'excited state', 'excretion', 'exocrine gland', 'exon', 'exons', 'exoplanet',
  'exoplanets', 'exoskeleton', 'exosphere', 'exothermic', 'exothermic reaction', 'exploit',
  'exploits', 'express', 'ext4', 'extinction', 'extract transform load', 'extrinsic semiconductor',
  'eye', 'f orbital', 'facade pattern', 'factory pattern', 'family', 'faraday constant',
  'faraday\'s law of electromagnetic induction', 'faraday\'s laws of electrolysis', 'fasciola', 'fastapi', 'fatty acid', 'fatty acids',
  'fault', 'fauna', 'feature engineering', 'feedback mechanism', 'feedforward neural network', 'feldspar',
  'fenwick tree', 'fermion', 'fern', 'ferns', 'ferromagnetism', 'fertilization',
  'fetus', 'feudalism', 'fibonacci heap', 'fibonacci sequence', 'fibrin', 'fibrinogen',
  'fibrous root', 'filament', 'file system', 'file systems', 'file transfer protocol', 'fine-tuning',
  'finite state machine', 'firewall', 'firewalls', 'firmware', 'first law of thermodynamics', 'first normal form',
  'first order reaction', 'first-class function', 'first-come first-served', 'fishes', 'flagellates', 'flash memory',
  'flask', 'flatworms', 'flip-flop', 'flip-flops', 'float', 'floating point',
  'flora', 'flotation', 'flower', 'flowers', 'floyd-warshall', 'floyd-warshall algorithm',
  'fluid', 'fluid dynamics', 'fluid mechanics', 'fluid statics', 'fluids', 'flux',
  'foetus', 'follicle-stimulating hormone', 'follicular phase', 'folliculogenesis', 'food chain', 'food web',
  'for loop', 'force', 'force on conductor', 'forced oscillation', 'forces', 'ford-fulkerson algorithm',
  'forebrain', 'foreign key', 'formal charge', 'formaldehyde', 'formic acid', 'forward bias',
  'forward proxy', 'fossil', 'fossil fuels', 'fossils', 'founder effect', 'fourier transform',
  'fovea', 'fragmentation', 'frameshift mutation', 'free radical', 'free-body diagram', 'freezing point',
  'freezing point depression', 'french revolution', 'frequency', 'friction', 'friedel-crafts reaction', 'fringe width',
  'frontend', 'froth floatation', 'fructose', 'fruit', 'fruiting bodies', 'fruiting body',
  'fsh', 'fsm', 'ftp', 'fucus', 'fuel cell', 'full stack',
  'full-wave rectifier', 'function', 'functional group', 'functional groups', 'functional programming', 'functions',
  'fundamental frequency', 'fungi', 'fungus', 'future', 'futures', 'gaba',
  'galactose', 'galaxies', 'galaxy', 'gallbladder', 'galvanic cell', 'galvanization',
  'gamete', 'gametes', 'gamma decay', 'gamma rays', 'gan', 'gangue',
  'garbage collection', 'garbage collector', 'gas', 'gas exchange', 'gastric gland', 'gastric juice',
  'gastropoda', 'gastrula', 'gastrulation', 'gated recurrent unit', 'gateway', 'gauss',
  'gauss\'s law', 'gaussian distribution', 'gay-lussac\'s law', 'gel electrophoresis', 'gelidium', 'genai',
  'gene', 'gene flow', 'general relativity', 'generative adversarial network', 'generative ai', 'generator',
  'generators', 'generic name', 'generics', 'genes', 'genetic code', 'genetic drift',
  'genetics', 'genotype', 'genus', 'geological time scale', 'geology', 'geometric isomerism',
  'geometric optics', 'geostationary satellite', 'geotropism', 'germ layers', 'germination', 'gestation',
  'gibberellic acid', 'gibberellin', 'gibberellins', 'gibbs free energy', 'ginkgo', 'git',
  'github', 'gitlab', 'glacier', 'glaciers', 'glial cells', 'global warming',
  'globe', 'glomerulus', 'glucagon', 'glucose', 'gluon', 'glycogen',
  'golang', 'google cloud', 'gpt', 'gpu', 'gradient', 'gradient descent',
  'graham\'s law of diffusion', 'grana', 'granite', 'granulocyte', 'granum', 'graph',
  'graph theory', 'graphics processing unit', 'graphql', 'graphs', 'gravitation', 'gravitational constant',
  'gravitational field', 'gravitational force', 'gravitational potential', 'gravitational potential energy', 'gravitropism', 'gravity',
  'greedy algorithm', 'greedy algorithms', 'green algae', 'greenhouse effect', 'greenhouse gases', 'grignard reagent',
  'ground state', 'groundwater', 'growth hormone', 'grpc', 'gru', 'guanine',
  'guard cell', 'guard cells', 'gui', 'gupta empire', 'guttation', 'gymnosperm',
  'gymnospermae', 'gymnosperms', 'gynoecium', 'habitat', 'habituation', 'half-life',
  'half-wave rectifier', 'halide', 'haloalkane', 'halogens', 'halting problem', 'harappa',
  'hard disk', 'hard disk drive', 'hardware', 'hardy-weinberg principle', 'harmonic', 'harmonics',
  'hash function', 'hash functions', 'hash index', 'hash map', 'hash set', 'hash table',
  'hash tables', 'hashing', 'hashmap', 'hashmaps', 'haskell', 'hatch-slack pathway',
  'haversian canal', 'hdd', 'heap', 'heaps', 'heapsort', 'heart',
  'heartwood', 'heat', 'heat capacity', 'heat transfer', 'heisenberg uncertainty principle', 'helicase',
  'helper t cell', 'hemisphere', 'hemoglobin', 'henderson-hasselbalch equation', 'henle\'s loop', 'hepatic portal vein',
  'heptane', 'herbarium', 'herbivore', 'herbivores', 'hess\'s law', 'heterogeneous catalysis',
  'heterogeneous mixture', 'heterozygous', 'hexane', 'hibernation', 'higgs boson', 'higher-order function',
  'higher-order functions', 'hill reaction', 'hindbrain', 'hinge joint', 'hippocampus', 'histamine',
  'histone acetylation', 'hmac', 'homeostasis', 'homo sapiens', 'homogeneous catalysis', 'homogeneous mixture',
  'homologous organs', 'homozygous', 'hooke\'s law', 'horizontal partitioning', 'hormone', 'hormones',
  'hornwort', 'horsetail', 'host', 'html', 'http', 'http/2',
  'http/3', 'https', 'hubble\'s law', 'huckel\'s rule', 'humidity', 'hund\'s rule',
  'hurricane', 'huygens\' principle', 'hyaline cartilage', 'hybrid kernel', 'hybridization', 'hydra',
  'hydraulic press', 'hydride', 'hydrocarbon', 'hydrocarbons', 'hydrochloric acid', 'hydrogen bond',
  'hydrogen bonding', 'hydrogen bonds', 'hydrogen spectrum', 'hydrophily', 'hydrosphere', 'hydrostatic pressure',
  'hydrotropism', 'hyper-threading', 'hyperconjugation', 'hyperparameter', 'hyperparameter tuning', 'hyperpolarization',
  'hypertext transfer protocol', 'hypervisor', 'hyphae', 'hypothalamus', 'hypothesis testing', 'hysteresis',
  'iaa', 'iaas', 'ideal gas', 'ideal gas equation', 'ideal gas law', 'iga',
  'igd', 'ige', 'igg', 'igm', 'igneous rock', 'igneous rocks',
  'ileum', 'image classification', 'image segmentation', 'immune system', 'immunity', 'immunization',
  'immunoglobulin', 'immutability', 'impedance', 'imperative programming', 'imperialism', 'imprinting',
  'impulse', 'in situ conservation', 'incisor', 'incomplete dominance', 'incus', 'indefinite integral',
  'indexing', 'indicator', 'indicators', 'indole-3-acetic acid', 'inducer', 'inductance',
  'inductive effect', 'inductive reactance', 'inductor', 'indus valley civilization', 'industrial revolution', 'inertia',
  'inflammation', 'information security', 'infosec', 'infrared', 'infrasonic', 'infrastructure as a service',
  'inheritance', 'innate immunity', 'inner core', 'inner transition elements', 'inode', 'inodes',
  'inorganic chemistry', 'insect', 'insecta', 'insects', 'insertion sort', 'instance',
  'instances', 'instantaneous velocity', 'instinct', 'instruction pipelining', 'instruction register', 'instruction set',
  'instruction set architecture', 'insulator', 'insulin', 'integer', 'integers', 'integral calculus',
  'integration', 'integration testing', 'inter-process communication', 'intercostal muscles', 'interface', 'interfaces',
  'interference', 'interferon', 'interferons', 'internal energy', 'internal resistance', 'internet protocol',
  'internode', 'interpreted language', 'interpreter', 'interpreters', 'interrupt', 'interrupt handler',
  'interrupts', 'intrinsic semiconductor', 'intron', 'introns', 'inversion', 'invertebrata',
  'invertebrates', 'inverted index', 'ion', 'ionic bond', 'ionic bonding', 'ionic bonds',
  'ionic radius', 'ionization energy', 'ions', 'ip', 'ip address', 'ipc',
  'ipv4', 'ipv6', 'iris', 'isa', 'islets of langerhans', 'isobar',
  'isobaric process', 'isobars', 'isochoric process', 'isolated system', 'isolation', 'isomer',
  'isomerism', 'isomers', 'isothermal process', 'isotone', 'isotones', 'isotope',
  'isotopes', 'iteration', 'iterator', 'iterators', 'java', 'javascript',
  'jejunum', 'jellyfish', 'jet stream', 'jit', 'jit compiler', 'joint',
  'joints', 'joule', 'joule\'s heating', 'json', 'json web token', 'jupiter',
  'just-in-time compiler', 'jwt', 'k-d tree', 'k-means', 'k-means clustering', 'k-nearest neighbors',
  'ka', 'kafka', 'kanban', 'kanban board', 'karyotype', 'kb',
  'kcl', 'kepler\'s first law', 'kepler\'s laws', 'kepler\'s second law', 'kepler\'s third law', 'kernel',
  'kernel space', 'kernels', 'ketone', 'ketones', 'keylogger', 'kidney',
  'kidneys', 'kinematics', 'kinetic energy', 'kinetic friction', 'kinetic molecular theory', 'kingdom',
  'kirchhoff\'s current law', 'kirchhoff\'s laws', 'kirchhoff\'s voltage law', 'klinefelter syndrome', 'kmp algorithm', 'knn',
  'knuth-morris-pratt algorithm', 'kotlin', 'kranz anatomy', 'kruskal', 'kruskal\'s algorithm', 'kubernetes',
  'kuiper belt', 'kvl', 'l1 cache', 'l2 cache', 'l3 cache', 'lac operon',
  'lactase', 'lactation', 'lacteal', 'lactose', 'lagging strand', 'lambda',
  'lambda expression', 'lambda expressions', 'lambda function', 'lamina', 'laminar flow', 'lan',
  'lanthanides', 'lanthanoids', 'laplace transform', 'large intestine', 'large language model', 'large language models',
  'larynx', 'latch', 'latches', 'latency', 'latent heat', 'latent heat of fusion',
  'latent heat of vaporization', 'latitude', 'lava', 'law of independent assortment', 'law of mass action', 'law of segregation',
  'laws of reflection', 'laws of refraction', 'lcr circuit', 'le chatelier\'s principle', 'leading strand', 'leaf',
  'leaf blade', 'league of nations', 'learning rate', 'leaves', 'led', 'leech',
  'leishmania', 'length contraction', 'lens', 'lens formula', 'lens maker\'s formula', 'lenses',
  'lenticel', 'lenticels', 'lenz\'s law', 'lepton', 'leptons', 'leukocyte',
  'leukocytes', 'lewis acid', 'lewis base', 'lewis structure', 'lh', 'lichen',
  'lichens', 'ligament', 'ligaments', 'ligand', 'ligands', 'light emitting diode',
  'light reactions', 'light year', 'light-dependent reactions', 'limbic system', 'limestone', 'limit',
  'limiting reactant', 'limiting reagent', 'limits', 'linear algebra', 'linear expansion', 'linear geometry',
  'linear momentum', 'linear regression', 'linear search', 'linkage', 'linked list', 'linked lists',
  'linting', 'linux', 'lipid', 'lipids', 'liquid', 'lithosphere',
  'liver', 'liver fluke', 'liverwort', 'liverworts', 'llm', 'load balancer',
  'load balancers', 'load balancing', 'local area network', 'logic gate', 'logic gates', 'logic programming',
  'logistic regression', 'london dispersion forces', 'long short-term memory', 'longitude', 'longitudinal wave', 'loop',
  'loop of henle', 'loops', 'lorentz force', 'lorentz transformation', 'loss function', 'lru cache',
  'lstm', 'lua', 'lunar eclipse', 'lunar phases', 'lung', 'lungs',
  'luteal phase', 'luteinizing hormone', 'lyman series', 'lymph', 'lymph node', 'lymph nodes',
  'lymphatic system', 'lymphocyte', 'lymphocytes', 'mac', 'mac address', 'machine code',
  'machine learning', 'macrophage', 'macrophages', 'magma', 'magna carta', 'magnetic declination',
  'magnetic dip', 'magnetic dipole', 'magnetic dipole moment', 'magnetic field', 'magnetic field lines', 'magnetic flux',
  'magnetic inclination', 'magnetic permeability', 'magnetic quantum number', 'magnetic susceptibility', 'magnetism', 'magnification',
  'malleus', 'malpighian corpuscle', 'maltase', 'maltose', 'malus\'s law', 'malware',
  'mammal', 'mammalia', 'mammals', 'man', 'man-in-the-middle attack', 'mangifera indica',
  'mantle', 'maratha empire', 'marble', 'mark-and-sweep', 'markov decision process', 'markovnikov\'s rule',
  'mars', 'mass', 'mass defect', 'mass flow hypothesis', 'mass number', 'matlab',
  'matrices', 'matrix', 'matter', 'maurya empire', 'max heap', 'maxwell\'s equations',
  'md5', 'mean', 'mean squared error', 'mechanical energy', 'mechanical wave', 'mechanics',
  'median', 'medulla oblongata', 'megasporangium', 'meiosis', 'melatonin', 'melting point',
  'memoization', 'memory', 'memory allocation', 'memory cell', 'memory leak', 'memory leaks',
  'meninges', 'menstrual cycle', 'menstruation', 'mercury', 'merge sort', 'mesi protocol',
  'meso compound', 'mesocarp', 'mesoderm', 'mesophyll', 'mesopotamia', 'mesosphere',
  'message authentication code', 'message broker', 'message queue', 'message queues', 'metabolism', 'metallic bond',
  'metalloids', 'metallurgy', 'metamorphic rock', 'metamorphic rocks', 'meteor', 'meteorite',
  'meteoroid', 'meter bridge', 'methane', 'methanol', 'method', 'method overloading',
  'method overriding', 'methods', 'methyl orange', 'metropolitan area network', 'mfa', 'microcontroller',
  'microcontrollers', 'microkernel', 'microprocessor', 'microprocessors', 'microscope', 'microservices',
  'microservices architecture', 'microsporangium', 'microvilli', 'microwaves', 'micturition', 'mid-ocean ridge',
  'midbrain', 'migration', 'milky way', 'min heap', 'mineral', 'mineral resources',
  'minerals', 'mirna', 'mirror equation', 'missense mutation', 'mitm', 'mitm attack',
  'mitosis', 'mixin', 'mixins', 'mixture', 'mixtures', 'ml',
  'mlp', 'mobility', 'mode', 'model-view-controller', 'model-view-viewmodel', 'modem',
  'mohenjo-daro', 'molality', 'molar', 'molar heat capacity', 'molar mass', 'molarity',
  'mole', 'mole fraction', 'molecular formula', 'molecular geometry', 'molecular orbital theory', 'molecule',
  'molecules', 'moles', 'mollusc', 'mollusca', 'mollusks', 'moment of inertia',
  'momentum', 'monarchy', 'monera', 'mongodb', 'monoclonal antibody', 'monocots',
  'monocotyledonae', 'monocyte', 'monocytes', 'monodentate ligand', 'monohybrid cross', 'monolithic architecture',
  'monolithic kernel', 'monomer', 'monomers', 'monosaccharide', 'monosaccharides', 'monosomy',
  'monsoon', 'moon', 'moraine', 'morphology', 'morula', 'mosfet',
  'moss', 'mosses', 'motherboard', 'motion', 'moving coil galvanometer', 'mrna',
  'mrna processing', 'mucor', 'mucus', 'mughal empire', 'multi-factor authentication', 'multi-head attention',
  'multicore', 'multicore processor', 'multilayer perceptron', 'multiple alleles', 'multiplexer', 'multiprocessing',
  'multithreading', 'muscle', 'muscles', 'museum', 'museums', 'mutagen',
  'mutation', 'mutations', 'mutex', 'mutexes', 'mutual inductance', 'mutualism',
  'mvc', 'mvvm', 'mycelium', 'mycorrhiza', 'mycorrhizae', 'myelin sheath',
  'myofibril', 'myofibrils', 'myoglobin', 'myosin', 'mysql', 'n-type semiconductor',
  'nand gate', 'naphthalene', 'nasal cavity', 'national park', 'nationalism', 'natural gas',
  'natural language processing', 'natural resources', 'natural selection', 'nebula', 'nebulae', 'nematoda',
  'nematodes', 'neo4j', 'nephron', 'nephrons', 'neptune', 'nernst equation',
  'nerve cell', 'nerve impulse', 'nervous system', 'network', 'network interface card', 'network layer',
  'network socket', 'network sockets', 'network switch', 'networking', 'networks', 'neural network',
  'neural networks', 'neuroglia', 'neuron', 'neurons', 'neurospora', 'neurotransmitter',
  'neurotransmitters', 'neutral oxide', 'neutralization', 'neutrino', 'neutron', 'neutron star',
  'neutrons', 'neutrophil', 'neutrophils', 'newsql', 'newton\'s first law', 'newton\'s law of cooling',
  'newton\'s laws of motion', 'newton\'s second law', 'newton\'s third law', 'next-generation sequencing', 'ngs', 'nic',
  'niche', 'nitrate', 'nitrile', 'nitriles', 'nitrite', 'nitro compound',
  'nitrobenzene', 'nitrogen cycle', 'nitrogen fixation', 'nlp', 'noble gases', 'node',
  'nodejs', 'nodes', 'nodes of ranvier', 'nomenclature', 'non-conservative force', 'non-cooperation movement',
  'non-renewable resources', 'nonane', 'nonpolar bond', 'nonpolar molecule', 'nonsense mutation', 'nor gate',
  'noradrenaline', 'norepinephrine', 'normal distribution', 'normal force', 'normality', 'northern blot',
  'nosql', 'not gate', 'notochord', 'np-complete', 'np-hard', 'npn transistor',
  'ntfs', 'nuclear fission', 'nuclear force', 'nuclear fusion', 'nuclear reactor', 'nucleic acid',
  'nucleic acids', 'nucleophile', 'nucleophilic addition', 'nucleoside', 'nucleotide', 'nucleotides',
  'nucleus', 'null hypothesis', 'null pointer', 'null pointer exception', 'nylon', 'nylon 66',
  'oauth', 'oauth 2.0', 'object', 'object detection', 'object-oriented programming', 'objects',
  'observer pattern', 'octahedral', 'octane', 'octet rule', 'octree', 'oesophagus',
  'ohm', 'ohm\'s law', 'okazaki fragment', 'okazaki fragments', 'olap', 'oltp',
  'omnivore', 'omnivores', 'oogenesis', 'oop', 'oort cloud', 'open addressing',
  'open id connect', 'open shortest path first', 'open system', 'operating system', 'operating systems', 'operator',
  'operon', 'optic nerve', 'optical activity', 'optical fiber', 'optical isomerism', 'optics',
  'optimistic concurrency control', 'or gate', 'oracle database', 'oral cavity', 'orbital', 'orbital velocity',
  'orbitals', 'order', 'order of reaction', 'ore', 'ores', 'organ of corti',
  'organic chemistry', 'organogenesis', 'origin of replication', 'oscillation', 'oscillations', 'osi model',
  'osmoregulation', 'osmosis', 'osmotic pressure', 'ospf', 'osteichthyes', 'osteoblast',
  'osteoclast', 'osteocyte', 'out-of-order execution', 'outer core', 'ova', 'ovaries',
  'ovary', 'overfitting', 'overloading', 'overriding', 'overtone', 'overtones',
  'ovulation', 'ovule', 'ovules', 'ovum', 'oxidation', 'oxidation number',
  'oxidation state', 'oxide', 'oxidizing agent', 'oxygen transport', 'oxyhemoglobin', 'oxytocin',
  'ozone layer', 'p orbital', 'p versus np', 'p wave', 'p-type semiconductor', 'p-value',
  'paas', 'packet', 'packet switching', 'packets', 'page fault', 'page faults',
  'page table', 'paging', 'palisade parenchyma', 'pancreas', 'pancreatic juice', 'pancreatic lipase',
  'pangea', 'panthera leo', 'panthera tigris', 'parallel axis theorem', 'parallel plate capacitor', 'parallel venation',
  'paramagnetism', 'paramecium', 'parasite', 'parasitism', 'parasympathetic nervous system', 'parathyroid gland',
  'parathyroid hormone', 'parsec', 'parthenogenesis', 'partial derivative', 'particle accelerator', 'parts per million',
  'parturition', 'pascal\'s law', 'pascal\'s principle', 'paschen series', 'passive immunity', 'path function',
  'pauli exclusion principle', 'paxos', 'pca', 'pcb', 'pcr', 'pct',
  'peak value', 'penetration testing', 'penicillium', 'pentane', 'pep carboxylase', 'pepsin',
  'pepsinogen', 'peptidase', 'peptide', 'peptide bond', 'peptidyl transferase', 'percentage yield',
  'perceptron', 'pericarp', 'pericycle', 'period', 'periodic law', 'periodic motion',
  'periodic table', 'peripheral nervous system', 'peristalsis', 'perl', 'permittivity', 'permutation',
  'perpendicular axis theorem', 'petal', 'petals', 'petiole', 'petroleum', 'pfund series',
  'ph', 'ph scale', 'phaeophyceae', 'phagocyte', 'phagocytes', 'phagocytosis',
  'pharynx', 'phase diagram', 'phellem', 'phellogen', 'phenol', 'phenolphthalein',
  'phenols', 'phenotype', 'pheromone', 'pheromones', 'phishing', 'phloem',
  'phloem fibers', 'phloem parenchyma', 'phloem translocation', 'phosphate', 'phosphodiester bond', 'phospholipid',
  'phosphorus cycle', 'photodiode', 'photoelectric effect', 'photolysis', 'photon', 'photons',
  'photoperiod', 'photoperiodism', 'photophosphorylation', 'photorespiration', 'photosynthesis', 'photosystem i',
  'photosystem ii', 'phototropism', 'php', 'phycomycetes', 'phyllotaxy', 'phylogeny',
  'phylum', 'physical layer', 'physical optics', 'physics', 'physiology', 'pi bond',
  'pia mater', 'pineal gland', 'pinna', 'pinus', 'pipe', 'pipelining',
  'pipes', 'pisces', 'pistil', 'pisum sativum', 'pituitary gland', 'pivot joint',
  'pki', 'placenta', 'plaintext', 'planaria', 'plane mirror', 'plant',
  'plantae', 'plants', 'plasma', 'plasma cell', 'plasmid', 'plasmids',
  'plasmodium', 'plasmolysis', 'plate tectonics', 'platelet', 'platelets', 'platform as a service',
  'platyhelminthes', 'pleiotropy', 'plumule', 'pluto', 'pn junction', 'pn junction diode',
  'pnp transistor', 'pns', 'poh', 'point mutation', 'pointer', 'pointers',
  'poiseuille\'s law', 'polar bond', 'polar molecule', 'polarization', 'pollen', 'pollen grain',
  'pollen grains', 'pollen tube', 'pollination', 'poly-a tail', 'polydentate ligand', 'polyethylene',
  'polygenic inheritance', 'polymer', 'polymerase chain reaction', 'polymerization', 'polymers', 'polymorphism',
  'polypeptide', 'polyploidy', 'polypropylene', 'polysaccharide', 'polysaccharides', 'polysiphonia',
  'polystyrene', 'polyvinyl chloride', 'pons', 'population density', 'porifera', 'port',
  'ports', 'posterior pituitary', 'postgresql', 'potential difference', 'potential energy', 'potentiometer',
  'power', 'power factor', 'power of lens', 'powershell', 'ppm', 'precipitation',
  'predation', 'predator', 'premolar', 'presentation layer', 'pressure', 'pressure flow hypothesis',
  'prim', 'prim\'s algorithm', 'primary amine', 'primary key', 'primary productivity', 'primary structure',
  'prime meridian', 'prime number', 'prime numbers', 'principal component analysis', 'principal quantum number', 'prion',
  'prions', 'priority queue', 'priority queues', 'prism', 'private key', 'probability',
  'probability distribution', 'procedural programming', 'process', 'process control block', 'process scheduling', 'processes',
  'producer', 'producers', 'profiling', 'progesterone', 'program counter', 'projectile motion',
  'prokaryote', 'prokaryotes', 'prolactin', 'prom', 'promise', 'promises',
  'promoter', 'prompt engineering', 'proof of stake', 'proof of work', 'propane', 'propanol',
  'propene', 'propyne', 'protein', 'proteins', 'prothrombin', 'protista',
  'protocol', 'protocols', 'proton', 'protons', 'prototype pattern', 'protozoa',
  'protozoans', 'proximal convoluted tubule', 'proxy pattern', 'proxy server', 'psi', 'psii',
  'pteridophyta', 'pteridophyte', 'pteridophytes', 'pth', 'ptyalin', 'public key',
  'public key infrastructure', 'public-key cryptography', 'puccinia', 'pull request', 'pulmonary artery', 'pulmonary vein',
  'pulsar', 'punnett square', 'pupil', 'pure function', 'pure functions', 'purine',
  'purines', 'purkinje fibers', 'pvc', 'pyramid of biomass', 'pyramid of energy', 'pyrimidine',
  'pyrimidines', 'python', 'q-learning', 'quadtree', 'quantization of charge', 'quantum',
  'quantum entanglement', 'quantum mechanics', 'quantum number', 'quantum numbers', 'quantum physics', 'quantum tunneling',
  'quark', 'quarks', 'quartz', 'quasar', 'quaternary structure', 'queue',
  'queues', 'quicksort', 'quit india movement', 'r language', 'rabbitmq', 'rabin-karp algorithm',
  'race condition', 'race conditions', 'racemic mixture', 'radiation', 'radicle', 'radio waves',
  'radioactivity', 'radius of gyration', 'radix sort', 'radix tree', 'raft consensus algorithm', 'rag',
  'ram', 'random access memory', 'random forest', 'random variable', 'range of projectile', 'ransomware',
  'rate constant', 'rate law', 'ray optics', 'rbac', 'rbc', 'rdbms',
  'react', 'reactance', 'reaction quotient', 'reaction rate', 'read-only memory', 'real gas',
  'recessive allele', 'recombinant dna', 'recombination', 'rectified linear unit', 'rectifier', 'rectum',
  'recurrent neural network', 'recursion', 'recursive', 'red algae', 'red blood cell', 'red blood cells',
  'red-black tree', 'red-black trees', 'redis', 'redox', 'redox reaction', 'redshift',
  'reducing agent', 'reduction', 'refactoring', 'reference', 'reference counting', 'references',
  'refining', 'reflection', 'reflex action', 'reflex arc', 'refraction', 'refractive index',
  'refractory period', 'refrigerator', 'register', 'registers', 'regression', 'regularization',
  'reinforcement learning', 'relational database', 'relational databases', 'relative density', 'relative lowering of vapour pressure', 'relativity',
  'relu', 'remote procedure call', 'renaissance', 'renal cortex', 'renal medulla', 'renal pelvis',
  'renewable resources', 'renin', 'replication', 'repolarization', 'repressor', 'reproduction',
  'reptile', 'reptiles', 'reptilia', 'republic', 'residual volume', 'resistance',
  'resistivity', 'resistors in parallel', 'resistors in series', 'resolving power', 'resonance', 'resonance effect',
  'resonance structures', 'resonant frequency', 'respiration', 'rest api', 'restful api', 'resting potential',
  'restoring force', 'restriction endonuclease', 'restriction enzyme', 'reticulate venation', 'retina', 'retrieval-augmented generation',
  'reverse bias', 'reverse proxy', 'reynolds number', 'rhizobium', 'rhizopus', 'rhodophyceae',
  'rhodopsin', 'ribosome', 'ribosomes', 'richter scale', 'rigid body', 'risc',
  'risc-v', 'rlhf', 'rms value', 'rna', 'rna polymerase', 'rna primer',
  'rna splicing', 'rnn', 'roasting', 'rock cycle', 'rods', 'role-based access control',
  'rollback', 'rolling friction', 'rolling without slipping', 'rom', 'roman empire', 'root',
  'root cap', 'root hair', 'root hairs', 'root nodule', 'root nodules', 'root pressure',
  'rootkit', 'roots', 'rotational motion', 'round robin', 'round-robin scheduling', 'roundworm',
  'router', 'routers', 'routing', 'routing algorithm', 'routing table', 'rpc',
  'rrna', 'rsa', 'rsa algorithm', 'rubisco', 'ruby', 'russian revolution',
  'rust', 'rusting', 'rutherford model', 'rydberg constant', 's orbital', 's wave',
  'saas', 'saliva', 'salivary amylase', 'salivary gland', 'salivary glands', 'salt',
  'salt bridge', 'salt hydrolysis', 'sandstone', 'sanger sequencing', 'sapiens', 'saponification',
  'sapwood', 'sarcomere', 'sarcomeres', 'satellite', 'satellites', 'saturated fatty acid',
  'saturated solution', 'saturn', 'satyagraha', 'scala', 'scheduling algorithm', 'schema',
  'schrodinger equation', 'schwann cell', 'schwann cells', 'scrum', 'scrum framework', 'sdlc',
  'sea anemone', 'sea cucumber', 'sea urchin', 'second law of thermodynamics', 'second normal form', 'second order reaction',
  'secondary amine', 'secondary structure', 'secure shell', 'secure sockets layer', 'sedimentary rock', 'sedimentary rocks',
  'seed', 'seed coat', 'seeds', 'segment tree', 'segmentation', 'seismic wave',
  'seismic waves', 'selection sort', 'selective reabsorption', 'self-attention', 'self-attention mechanism', 'self-inductance',
  'self-pollination', 'semantics', 'semaphore', 'semaphores', 'semi-supervised learning', 'semicircular canals',
  'semiconductor', 'semiconductors', 'semiconservative replication', 'sepal', 'sepals', 'separate chaining',
  'sepoy mutiny', 'serotonin', 'serum', 'server', 'serverless', 'serverless computing',
  'servers', 'service-oriented architecture', 'session layer', 'set theory', 'sex chromosomes', 'sex linkage',
  'sex-linked inheritance', 'sexual reproduction', 'sha-256', 'shale', 'sharding', 'shared memory',
  'shell', 'shielding effect', 'shm', 'shoot', 'shortest job first', 'side effect',
  'side effects', 'sieve tube', 'sigma bond', 'sigmoid', 'sigmoid function', 'silent mutation',
  'simple harmonic motion', 'simple leaf', 'simple mail transfer protocol', 'simple pendulum', 'single slit diffraction', 'single-stranded binding protein',
  'singleton pattern', 'singly linked list', 'singularity', 'sinoatrial node', 'sirna', 'site reliability engineering',
  'skeletal muscle', 'skeleton', 'skip list', 'slag', 'slate', 'sliding filament theory',
  'sliding window', 'sliding window protocol', 'slime moulds', 'small intestine', 'smart contract', 'smart contracts',
  'smelting', 'smooth muscle', 'smtp', 'sn1 reaction', 'sn2 reaction', 'snell\'s law',
  'soa', 'soc', 'social engineering', 'socialism', 'socket', 'sockets',
  'softmax', 'softmax function', 'software', 'software as a service', 'software development life cycle', 'software engineering',
  'soil conservation', 'soil erosion', 'solar cell', 'solar eclipse', 'solar system', 'solenoid',
  'solid', 'solid principles', 'solid state drive', 'solid-state drive', 'solubility', 'solubility product',
  'solute', 'solution', 'solutions', 'solvent', 'soma', 'somatostatin',
  'sorting algorithm', 'sound', 'sound wave', 'source and sink', 'source code', 'southern blot',
  'sp hybridization', 'sp2 hybridization', 'sp3 hybridization', 'sp3d hybridization', 'sp3d2 hybridization', 'space complexity',
  'spacetime', 'spear phishing', 'special relativity', 'speciation', 'species', 'species richness',
  'specific epithet', 'specific heat', 'specific heat capacity', 'spectrochemical series', 'speed', 'speed of sound',
  'sperm', 'spermatogenesis', 'spermatozoa', 'spherical mirror', 'spider', 'spin quantum number',
  'spinal cord', 'spinlock', 'spirogyra', 'splay tree', 'spleen', 'spliceosome',
  'sponge', 'sponges', 'spongilla', 'spongy bone', 'spongy parenchyma', 'spontaneity',
  'sporangiospores', 'sporozoans', 'sporulation', 'spring boot', 'spring constant', 'spyware',
  'sql', 'sql injection', 'sqli', 'sqlite', 'sram', 'sre',
  'ssb', 'ssd', 'ssh', 'ssl', 'stack', 'stack overflow',
  'stack pointer', 'stacks', 'stamen', 'stamens', 'standard deviation', 'standard enthalpy of formation',
  'standard hydrogen electrode', 'standard model', 'standard reduction potential', 'standing wave', 'standing waves', 'stapes',
  'star', 'starch', 'starfish', 'stars', 'state function', 'static code analysis',
  'static friction', 'static typing', 'stationary wave', 'stefan-boltzmann law', 'stem', 'step-down transformer',
  'step-up transformer', 'stereoisomerism', 'steroid', 'steroids', 'stigma', 'stochastic gradient descent',
  'stoichiometry', 'stokes\' law', 'stoma', 'stomach', 'stomata', 'stopping potential',
  'strategy pattern', 'stratigraphy', 'stratosphere', 'streamline flow', 'stroma', 'structural isomerism',
  'style', 'subduction zone', 'sublimation', 'subnet', 'subnet mask', 'substance',
  'sucrase', 'sucrose', 'suffix array', 'suffix tree', 'sulfate', 'sulfide',
  'sun', 'superconductor', 'superconductors', 'superficial expansion', 'supernova', 'superposition',
  'superposition principle', 'supersaturated solution', 'supervised learning', 'support vector machine', 'surface energy', 'surface tension',
  'surrogate key', 'surroundings', 'sustainability', 'sustainable development', 'svm', 'swaraj',
  'swift', 'switch statement', 'sycon', 'symbiosis', 'symmetric encryption', 'symmetric-key cryptography',
  'sympathetic nervous system', 'synapse', 'synapses', 'synaptic cleft', 'syngamy', 'synovial joint',
  'syntax', 'system bus', 'system call', 'system calls', 'system on a chip', 'systema naturae',
  'systematic', 'systematics', 'systole', 't cell', 't lymphocyte', 't3',
  't4', 'tabulation', 'taenia', 'tapeworm', 'taproot', 'taq polymerase',
  'tata box', 'taxa', 'taxon', 'taxonomic category', 'taxonomic hierarchy', 'taxonomist',
  'taxonomists', 'taxonomy', 'taylor series', 'tcp', 'tcp/ip', 'tcp/ip model',
  'tdd', 'tectonic plates', 'teeth', 'teflon', 'tegmen', 'telescope',
  'telomerase', 'telomere', 'telomeres', 'temperature', 'template metaprogramming', 'tendon',
  'tendons', 'tension', 'tensor processing unit', 'terminal velocity', 'ternary search', 'tertiary amine',
  'tertiary structure', 'terylene', 'tesla', 'test cross', 'test-driven development', 'testa',
  'testes', 'testis', 'testosterone', 'tetrahedral', 'thalamus', 'thallophyta',
  'thermal conductivity', 'thermal efficiency', 'thermal energy', 'thermal equilibrium', 'thermal expansion', 'thermodynamics',
  'thermometer', 'thermosphere', 'thigmotropism', 'third law of thermodynamics', 'third normal form', 'thrashing',
  'thread', 'threads', 'threshold frequency', 'thrombin', 'thrombocyte', 'thrombocytes',
  'throughput', 'thylakoid', 'thylakoids', 'thymine', 'thymus', 'thyroid gland',
  'thyroxine', 'tidal volume', 'time complexity', 'time dilation', 'titrant', 'titration',
  'tlb', 'tls', 'tokenization', 'toluene', 'tongue', 'tonsils',
  'topoisomerase', 'topological sort', 'topology', 'tornado', 'toroid', 'torque',
  'torricelli\'s law', 'total internal reflection', 'total lung capacity', 'tpu', 'trachea', 'tracheid',
  'tracheids', 'trait', 'traits', 'trajectory', 'transactions', 'transcription',
  'transcription factor', 'transcription factors', 'transformer', 'transformer architecture', 'transformers', 'transgenic organism',
  'transistor', 'transistors', 'transition elements', 'transition metals', 'transition state', 'translation',
  'translation lookaside buffer', 'translocation', 'transmission control protocol', 'transpiration', 'transpiration pull', 'transport layer',
  'transport layer security', 'transverse wave', 'treaty of versailles', 'tree', 'trees', 'trie',
  'tries', 'triglyceride', 'triglycerides', 'trigonal bipyramidal', 'trigonal planar', 'triple fusion',
  'triple point', 'trisomy', 'trna', 'trojan', 'trojan horse', 'trophic level',
  'trophic levels', 'tropic of cancer', 'tropic of capricorn', 'tropomyosin', 'troponin', 'troposphere',
  'trp operon', 'trypanosoma', 'trypsin', 'trypsinogen', 'tsunami', 'tubular secretion',
  'turbulent flow', 'turgor pressure', 'turing machine', 'turner syndrome', 'two pointers', 'two-phase commit',
  'two-phase locking', 'two-pointer technique', 'tympanic membrane', 'type checking', 'type inference', 'type-1 hypervisor',
  'type-2 hypervisor', 'typescript', 'typhoon', 'udp', 'uefi', 'ulothrix',
  'ultrafiltration', 'ultrasonic', 'ultraviolet', 'umbilical cord', 'underfitting', 'undirected graph',
  'uniform acceleration', 'uniform circular motion', 'union find', 'union-find', 'unique constraint', 'unique key',
  'unit testing', 'united nations', 'universal law of gravitation', 'unix', 'unsaturated fatty acid', 'unsaturated solution',
  'unsupervised learning', 'uracil', 'uranus', 'urea', 'ureotelic', 'ureter',
  'urethra', 'uric acid', 'uricotelic', 'urinary bladder', 'urine', 'user datagram protocol',
  'user space', 'ustilago', 'vaccination', 'vaccine', 'valence electron', 'valence electrons',
  'valency', 'van \'t hoff factor', 'van der waals equation', 'van der waals forces', 'vapor pressure', 'variable',
  'variables', 'variance', 'vascular bundle', 'vascular bundles', 'vascular cambium', 'vasopressin',
  'vcs', 'vector', 'vector database', 'vector space', 'vein', 'veins',
  'velocity', 'vena cava', 'venation', 'ventricle', 'venturi meter', 'venus',
  'vernalization', 'version control', 'version control system', 'vertebrata', 'vertebrates', 'vertical partitioning',
  'vestigial organs', 'villi', 'viroid', 'viroids', 'virtual machine', 'virtual machines',
  'virtual memory', 'virtual private network', 'virtualization', 'virus', 'viruses', 'viscosity',
  'visible spectrum', 'vital capacity', 'vitamin', 'vitamins', 'vocal cords', 'volcano',
  'volcanoes', 'volt', 'voltage', 'voltaic cell', 'voltmeter', 'volvox',
  'vpn', 'vsepr theory', 'vue', 'vulnerabilities', 'vulnerability', 'wal',
  'wan', 'water cycle', 'water harvesting', 'water potential', 'water table', 'waterfall model',
  'watt', 'wave', 'wave function', 'wave optics', 'wave velocity', 'wavefront',
  'wavelength', 'waves', 'wbc', 'weathering', 'web development', 'web3',
  'websocket', 'websockets', 'weight', 'weighted graph', 'western blot', 'wheatstone bridge',
  'while loop', 'white blood cell', 'white blood cells', 'white dwarf', 'wi-fi', 'wide area network',
  'wien\'s displacement law', 'wifi', 'wildlife sanctuary', 'wireless local area network', 'wlan', 'wolff-kishner reduction',
  'wood', 'word embedding', 'word embeddings', 'word2vec', 'work', 'work done',
  'work function', 'work-energy theorem', 'world war i', 'world war ii', 'worm', 'write-ahead logging',
  'x-rays', 'x86', 'x86-64', 'xml', 'xnor gate', 'xor gate',
  'xss', 'xylem', 'xylem vessel', 'xylene', 'yaml', 'ydse',
  'young\'s double-slit experiment', 'zeatin', 'zener diode', 'zero order reaction', 'zero-day', 'zero-day vulnerability',
  'zeroth law of thermodynamics', 'zfs', 'zoological park', 'zoological parks', 'zoophily', 'zoospores',
  'zygote'
]

function isStrictlyValidTerm(rawTerm) {
  if (!rawTerm || typeof rawTerm !== 'string') return false
  const clean = rawTerm.trim().replace(/^['"“‘]+|['"”’]+$/g, '')
  const ALLOWED_SHORT_TECH_TERMS = new Set(['ai', 'ml', 'ip', 'os', 'db', 'vm', 'ui', 'ux', 'io', 'c#', 'c', 'r'])
  if (clean.length < 2 || clean.length > 45) return false
  if (clean.length === 2 && !ALLOWED_SHORT_TECH_TERMS.has(clean.toLowerCase())) return false
  const lower = clean.toLowerCase()
  if (GENERIC_STOPWORDS_FILTER.has(lower)) return false
  if (/^\d+$/.test(clean)) return false

  const words = lower.split(/\s+/).filter(Boolean)
  if (words.length === 0) return false

  // 1-word terms: must not be an invalid connector, verb, or stopword
  if (words.length === 1) {
    const w = words[0]
    if (INVALID_CONNECTOR_WORDS.has(w) || INVALID_VERB_AND_ACTION_WORDS.has(w) || GENERIC_STOPWORDS_FILTER.has(w)) {
      return false
    }
    return true
  }

  // Multi-word terms:
  // Reject if first word or last word is a preposition, article, pronoun, or connector
  const firstWord = words[0]
  const lastWord = words[words.length - 1]
  if (INVALID_CONNECTOR_WORDS.has(firstWord) || INVALID_CONNECTOR_WORDS.has(lastWord)) {
    return false
  }

  // Reject if any word in the multi-word phrase is an invalid verb
  for (const w of words) {
    if (INVALID_VERB_AND_ACTION_WORDS.has(w)) {
      return false
    }
  }

  // If 2 words, reject if both words are generic stopwords
  if (words.length === 2 && GENERIC_STOPWORDS_FILTER.has(words[0]) && GENERIC_STOPWORDS_FILTER.has(words[1])) {
    return false
  }

  return true
}

function buildGlobalTermMap(terms = []) {
  const map = new Map()

  function addTerm(rawTerm, category, canonical) {
    if (!isStrictlyValidTerm(rawTerm)) return
    const str = rawTerm.trim().replace(/^['"“‘]+|['"”’]+$/g, '')
    const lower = str.toLowerCase()

    const canon = canonical || str
    const record = { term: canon, category: category || 'scientific_term' }
    if (!map.has(lower)) {
      map.set(lower, record)
    }

    const plurals = []
    if (!lower.endsWith('s')) {
      plurals.push(lower + 's')
      plurals.push(lower + 'es')
      plurals.push(lower + "'s")
      plurals.push(lower + "’s")
    }
    if (lower.endsWith('y') && lower.length > 3) {
      plurals.push(lower.slice(0, -1) + 'ies')
    }
    if (lower.endsWith('on') && lower.length > 3) {
      plurals.push(lower.slice(0, -2) + 'a')
    }
    if (lower.endsWith('us') && lower.length > 3) {
      plurals.push(lower.slice(0, -2) + 'i')
      if (lower === 'genus') plurals.push('genera')
    }

    for (const p of plurals) {
      if (isStrictlyValidTerm(p) && !map.has(p)) {
        map.set(p, record)
      }
    }
  }

  for (const p of KNOWN_PEOPLE_LIST) addTerm(p, 'person', p.charAt(0).toUpperCase() + p.slice(1))
  for (const s of KNOWN_SCIENTISTS_LIST) addTerm(s, 'scientist', s.charAt(0).toUpperCase() + s.slice(1))
  for (const loc of KNOWN_LOCATIONS_LIST) addTerm(loc, 'location', loc.charAt(0).toUpperCase() + loc.slice(1))
  for (const sc of CORE_SCIENCE_LIST) addTerm(sc, 'scientific_term', sc)

  for (const item of terms) {
    if (item?.term && typeof item.term === 'string') {
      addTerm(item.term, item.category || 'scientific_term', item.term)
    }
  }

  return map
}

function highlightDocumentText(value, terms, enabled, onWordClick, seenTerms) {
  const localSeen = seenTerms || new Set()
  const text = cleanDocumentText(String(value || ''))
  if (!text) return text
  if (!enabled) return text

  const termMap = buildGlobalTermMap(terms)
  const termPatterns = [...termMap.keys()]
    .filter(term => !GENERIC_STOPWORDS_FILTER.has(term.toLowerCase()) && term.length >= 3)
    .sort((a, b) => b.length - a.length)
    .map(term => term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))

  if (!termPatterns.length) return text

  const regex = new RegExp(
    `(^|[^\\p{L}\\p{N}])(${termPatterns.join('|')})(?=$|[^\\p{L}\\p{N}])`,
    'giu'
  )
  const matches = []
  for (const match of text.matchAll(regex)) {
    const prefix = match[1] || ''
    const matchedTerm = match[2]
    const lower = matchedTerm.toLowerCase()
    if (GENERIC_STOPWORDS_FILTER.has(lower) || lower.length < 3) continue

    const start = match.index + prefix.length
    const end = start + matchedTerm.length
    const termObj = termMap.get(lower)

    let category = termObj?.category || 'scientific_term'
    let canonicalTerm = termObj?.term || matchedTerm

    matches.push({
      start,
      end,
      matchedText: matchedTerm,
      canonicalTerm,
      category,
    })
  }

  if (!matches.length) return text

  // Sort and remove overlapping matches AND de-duplicate repeated terms
  matches.sort((a, b) => a.start - b.start)
  const nonOverlapping = []
  let lastEnd = 0

  for (const m of matches) {
    if (m.start >= lastEnd) {
      const canonKey = (m.canonicalTerm || m.matchedText).trim().toLowerCase()
      const rootKey = canonKey.replace(/['’]s$/, '').replace(/s$/, '').replace(/es$/, '').replace(/ies$/, 'y')

      if (localSeen) {
        if (localSeen.has(canonKey) || localSeen.has(rootKey)) {
          // Do not underline repeated occurrence in the same section
          continue
        }
        localSeen.add(canonKey)
        localSeen.add(rootKey)
      }

      nonOverlapping.push(m)
      lastEnd = m.end
    }
  }

  const fragments = []
  let cursor = 0

  for (const m of nonOverlapping) {
    if (m.start > cursor) {
      fragments.push(text.slice(cursor, m.start))
    }

    const className = m.category === 'scientist'
      ? 'scientist'
      : m.category === 'person'
      ? 'person'
      : m.category === 'location'
      ? 'location'
      : 'scientific-term'

    const prevBoundary = Math.max(
      text.lastIndexOf('.', m.start),
      text.lastIndexOf('?', m.start),
      text.lastIndexOf('!', m.start),
      text.lastIndexOf('\n', m.start)
    )
    const startIdx = prevBoundary >= 0 ? prevBoundary + 1 : 0
    const nextStops = ['.', '?', '!', '\n'].map(mark => text.indexOf(mark, m.end)).filter(index => index >= 0)
    const endIdx = nextStops.length ? Math.min(...nextStops) + 1 : text.length
    const sentence = text.slice(startIdx, endIdx).trim()

    fragments.push(
      <button
        type="button"
        key={`${m.start}-${m.matchedText}`}
        className={`clickable-term color-term ${className}`}
        onClick={event => onWordClick?.({
          word: m.canonicalTerm || m.matchedText,
          context: sentence,
          rect: event.currentTarget.getBoundingClientRect(),
        })}
        title={`Click for photo & reference: ${m.canonicalTerm || m.matchedText}`}
      >
        {m.matchedText}
      </button>
    )

    cursor = m.end
  }

  if (cursor < text.length) {
    fragments.push(text.slice(cursor))
  }

  return fragments
}

function flowStepText(value) {
  return String(value || '')
    .replace(/^\s*(?:step|stage)\s*\d+\s*[:.)-]\s*/i, '')
    .replace(/^\s*(?:part|section|topic|module)\s*\d+\s*[:.)-]?\s*/i, '')
    .trim()
}

const LEADING_JUNK_WORDS = new Set([
  'although', 'because', 'since', 'though', 'whereas', 'while', 'if', 'unless', 'until',
  'when', 'whenever', 'where', 'wherever', 'whether', 'as', 'after', 'before', 'to', 'for',
  'in', 'on', 'at', 'by', 'from', 'with', 'into', 'about', 'and', 'or', 'but', 'so', 'yet',
  'also', 'furthermore', 'moreover', 'however', 'therefore', 'thus', 'these', 'this', 'those', 'such'
])

const TRAILING_FILLERS = new Set([
  'a', 'an', 'the', 'to', 'of', 'for', 'with', 'and', 'or', 'is', 'are', 'was', 'were',
  'that', 'in', 'on', 'at', 'by', 'from', 'as', 'so', 'such', 'this', 'these',
  'which', 'where', 'when', 'while', 'also', 'into', 'than', 'then', 'not', 'but', 'has', 'have',
  'very', 'dark', 'light', 'bulky'
])

function extractConceptTitle(text) {
  if (!text) return ''
  let clean = String(text)
    .replace(/^\s*(?:step|stage)\s*\d+\s*[:.)-]\s*/i, '')
    .replace(/^\s*(?:part|section|topic|module)\s*\d+\s*[:.)-]?\s*/i, '')
    .replace(/^(?:the\s+user\s+has\s+to|it\s+is\s+clear\s+that|this\s+shows\s+that|we\s+can\s+see\s+that|the\s+source\s+explains\s+that|the\s+source\s+states\s+that|it\s+is\s+found\s+that|according\s+to\s+the\s+text)\s+/i, '')
    .split(/;|,\s*(?:if|when|while|otherwise|which|because|so\s+that)\b|\s+otherwise\b/i)[0]
    .trim()

  // Match clean definition subjects e.g. "Smelters is a very bulky..." -> "Smelters & Smelting"
  const isMatch = clean.match(/^([a-zA-Z\s]{3,35})\s+(?:is|are|was|were|refers to|means|consists of)\b/i)
  if (isMatch && isMatch[1]) {
    const subject = isMatch[1].trim()
    if (subject.split(/\s+/).length <= 4) {
      return toTitleCase(subject)
    }
  }

  let words = clean.split(/\s+/).filter(Boolean)
  // Strip leading conjunctions / prepositions
  while (words.length > 2 && LEADING_JUNK_WORDS.has(words[0].toLowerCase().replace(/[.,:;]+$/, ''))) {
    words.shift()
  }
  if (words.length > 2 && words[0].toLowerCase() === 'used' && words[1].toLowerCase() === 'for') {
    words = words.slice(2)
  }

  let slice = words.slice(0, Math.min(words.length, 5))
  while (slice.length > 1 && TRAILING_FILLERS.has(slice[slice.length - 1].toLowerCase().replace(/[.,:;]+$/, ''))) {
    slice.pop()
  }

  const title = slice.join(' ').replace(/[.,:;]+$/, '').trim()
  return title.length >= 3 ? toTitleCase(title) : 'Key Process Concept'
}

function cleanCompleteDescription(text, allSentences = []) {
  let cleaned = String(text || '').trim()
    .replace(/^(\d+(?:\.\d+)*\s*[:.\-–—]?\s*)/, '')
    .replace(/[“"'”’]/g, '')
    .trim()

  if (!cleaned) return ''

  const endsAbruptly = /(?:\b(?:so|such|and|or|to|for|with|of|that|is|are|in|on|by|from|as|such as|called|which|because)\b\s*|[,\-–—:;]\s*)$/i.test(cleaned)
  
  if (endsAbruptly || cleaned.length < 35) {
    const firstWords = cleaned.toLowerCase().split(/\s+/).slice(0, 3).join(' ')
    const fullMatch = allSentences.find(s => s.toLowerCase().includes(firstWords) && s.length > cleaned.length)
    if (fullMatch) {
      cleaned = fullMatch
    }
  }

  cleaned = cleaned.replace(/\s+(?:so|and|or|to|for|with|of|that|is|are|in|on|by|from|as|such as|called|which|because)\s*[.,:;]?$/i, '')

  if (!/[.!?]$/.test(cleaned)) {
    cleaned += '.'
  }

  return capitalizeSentenceStarts(cleaned)
}

function buildFlowStages(section, keyIdeas, topics, details, paragraphs, overview) {
  const stages = []
  const seenTitles = new Set()
  const allSentences = [
    overview,
    ...paragraphs,
    ...keyIdeas,
    ...topics.map(t => t.body),
    ...details.map(d => d.body)
  ].flatMap(text => String(text || '').split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(Boolean))

  const addStage = (titleCandidate, descCandidate) => {
    const title = extractConceptTitle(titleCandidate)
    if (!title || seenTitles.has(title.toLowerCase())) return
    const description = cleanCompleteDescription(descCandidate || titleCandidate, allSentences)
    if (!description || description.length < 15) return
    seenTitles.add(title.toLowerCase())
    stages.push({ title, description })
  }

  // 1. From subtopics if available
  for (const topic of topics) {
    if (topic.title && topic.body) {
      addStage(topic.title, topic.body)
    }
    if (stages.length >= 5) break
  }

  // 2. From mechanical deep dive if available
  if (stages.length < 3) {
    for (const item of details) {
      if (item.subheading && item.body) {
        addStage(item.subheading, item.body)
      }
      if (stages.length >= 5) break
    }
  }

  // 3. From process_hierarchy and process_details
  const modelHierarchy = section.process_hierarchy || []
  const modelDetails = section.process_details || []
  for (let i = 0; i < modelHierarchy.length; i++) {
    const rawStep = modelHierarchy[i]
    if (!rawStep) continue
    const rawDetail = modelDetails[i] || rawStep
    addStage(rawStep, rawDetail.length > rawStep.length + 10 ? rawDetail : (keyIdeas[i] || paragraphs[i] || rawDetail))
    if (stages.length >= 5) break
  }

  // 4. From keyIdeas
  if (stages.length < 3) {
    for (const idea of keyIdeas) {
      addStage(idea, idea)
      if (stages.length >= 5) break
    }
  }

  // 5. From paragraphs
  if (stages.length < 3) {
    for (const p of paragraphs) {
      const sentences = p.split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(s => s.length > 25)
      for (const s of sentences) {
        addStage(s, s)
        if (stages.length >= 4) break
      }
      if (stages.length >= 4) break
    }
  }

  return stages
}

function parseKeyTakeaways(rawTakeaways) {
  if (!rawTakeaways || !rawTakeaways.length) return []
  const items = Array.isArray(rawTakeaways) ? rawTakeaways : [rawTakeaways]
  return items.flatMap(item => {
    const text = String(item || '').trim()
    if (!text) return []
    if (text.includes(';') && text.split(';').filter(s => s.trim().length > 15).length >= 2) {
      return text.split(';').map(s => s.trim()).filter(s => s.length > 10)
    }
    if (items.length === 1 && text.length > 120) {
      const sentences = text.split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(s => s.length > 20)
      if (sentences.length >= 2) return sentences
    }
    return [text]
  }).filter(Boolean).map(capitalizeSentenceStarts)
}

function parseDocumentBlocks(rawText) {
  if (!rawText) return []
  const text = String(rawText).trim()
  if (!text) return []

  const lines = text.split('\n')
  const blocks = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]
    const trimmed = line.trim()

    if (!trimmed) {
      i++
      continue
    }

    // 1. Code Block: ```
    if (trimmed.startsWith('```')) {
      const codeLines = []
      i++
      while (i < lines.length && !lines[i].trim().startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      if (i < lines.length && lines[i].trim().startsWith('```')) i++
      blocks.push({
        type: 'code',
        content: codeLines.join('\n'),
      })
      continue
    }

    // 2. Table: lines starting with | and ending with |
    if (trimmed.startsWith('|') && trimmed.endsWith('|') && trimmed.length > 2) {
      const tableLines = []
      while (i < lines.length && lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
        tableLines.push(lines[i].trim())
        i++
      }
      if (tableLines.length >= 2) {
        const headerRow = tableLines[0].split('|').slice(1, -1).map(c => c.trim())
        const startRow = tableLines[1].includes('---') ? 2 : 1
        const dataRows = tableLines.slice(startRow).map(row => row.split('|').slice(1, -1).map(c => c.trim()))
        blocks.push({
          type: 'table',
          headers: headerRow,
          rows: dataRows,
        })
        continue
      }
    }

    // 3. Blockquote: > text
    if (trimmed.startsWith('>')) {
      const quoteLines = []
      while (i < lines.length && lines[i].trim().startsWith('>')) {
        quoteLines.push(lines[i].trim().replace(/^>\s*/, ''))
        i++
      }
      blocks.push({
        type: 'blockquote',
        content: quoteLines.join(' '),
      })
      continue
    }

    // 4. Bullet List: lines starting with * , - , + , • , ‣ , ⁃
    if (/^[\s]*[*\-+•‣⁃]\s+/.test(line)) {
      const listItems = []
      while (i < lines.length && (/^[\s]*[*\-+•‣⁃]\s+/.test(lines[i]) || (lines[i].startsWith('  ') && listItems.length > 0))) {
        if (/^[\s]*[*\-+•‣⁃]\s+/.test(lines[i])) {
          listItems.push(lines[i].replace(/^[\s]*[*\-+•‣⁃]\s+/, '').trim())
        } else if (listItems.length > 0) {
          listItems[listItems.length - 1] += ' ' + lines[i].trim()
        }
        i++
      }
      blocks.push({
        type: 'bullet_list',
        items: listItems,
      })
      continue
    }

    // 5. Numbered List: lines starting with 1. , 2. , (a) , a)
    if (/^[\s]*(?:\d+\.|\(\d+\)|\([a-zA-Z]\)|[a-zA-Z]\))\s+/.test(line)) {
      const listItems = []
      while (i < lines.length && (/^[\s]*(?:\d+\.|\(\d+\)|\([a-zA-Z]\)|[a-zA-Z]\))\s+/.test(lines[i]) || (lines[i].startsWith('  ') && listItems.length > 0))) {
        if (/^[\s]*(?:\d+\.|\(\d+\)|\([a-zA-Z]\)|[a-zA-Z]\))\s+/.test(lines[i])) {
          listItems.push(lines[i].replace(/^[\s]*(?:\d+\.|\(\d+\)|\([a-zA-Z]\)|[a-zA-Z]\))\s+/, '').trim())
        } else if (listItems.length > 0) {
          listItems[listItems.length - 1] += ' ' + lines[i].trim()
        }
        i++
      }
      blocks.push({
        type: 'numbered_list',
        items: listItems,
      })
      continue
    }

    // 6. Subheading: ###, ##, #
    if (/^#{1,4}\s+/.test(trimmed)) {
      blocks.push({
        type: 'heading',
        content: trimmed.replace(/^#{1,4}\s+/, ''),
      })
      i++
      continue
    }

    // 7. Regular paragraph (collecting lines until blank line or special block)
    const pLines = []
    while (
      i < lines.length &&
      lines[i].trim() &&
      !lines[i].trim().startsWith('```') &&
      !lines[i].trim().startsWith('>') &&
      !/^[\s]*[*\-+•‣⁃]\s+/.test(lines[i]) &&
      !/^[\s]*(?:\d+\.|\(\d+\)|\([a-zA-Z]\)|[a-zA-Z]\))\s+/.test(lines[i]) &&
      !/^#{1,4}\s+/.test(lines[i].trim()) &&
      !(lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|'))
    ) {
      pLines.push(lines[i].trim())
      i++
    }
    const paraText = pLines.join(' ')
    if (paraText) {
      blocks.push({
        type: 'paragraph',
        content: paraText,
      })
    }
  }

  return blocks
}

function renderDocumentContent(content, renderText) {
  if (!content) return null
  const rawList = Array.isArray(content) ? content : [content]
  const allBlocks = rawList.flatMap(item => parseDocumentBlocks(item))

  if (allBlocks.length === 0) return null

  return allBlocks.map((block, idx) => {
    switch (block.type) {
      case 'code':
        return (
          <pre key={idx} className="document-code-block">
            <code>{block.content}</code>
          </pre>
        )
      case 'table':
        return (
          <div key={idx} className="document-table-wrap">
            <table className="document-table">
              {block.headers && block.headers.length > 0 && (
                <thead>
                  <tr>
                    {block.headers.map((h, hIdx) => (
                      <th key={hIdx}>{renderText(h)}</th>
                    ))}
                  </tr>
                </thead>
              )}
              <tbody>
                {block.rows.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((cell, cIdx) => (
                      <td key={cIdx}>{renderText(cell)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      case 'blockquote':
        return (
          <blockquote key={idx} className="document-blockquote">
            <p>{renderText(block.content)}</p>
          </blockquote>
        )
      case 'bullet_list':
        return (
          <ul key={idx} className="document-bullet-list">
            {block.items.map((item, itemIdx) => (
              <li key={itemIdx}>{renderText(item)}</li>
            ))}
          </ul>
        )
      case 'numbered_list':
        return (
          <ol key={idx} className="document-numbered-list">
            {block.items.map((item, itemIdx) => (
              <li key={itemIdx}>{renderText(item)}</li>
            ))}
          </ol>
        )
      case 'heading':
        return (
          <h4 key={idx} className="document-subheading">
            {renderText(block.content)}
          </h4>
        )
      case 'paragraph':
      default:
        const isShort = block.content.length < 110
        return (
          <p
            key={idx}
            className={`document-paragraph ${isShort ? 'document-paragraph-short' : ''}`}
          >
            {renderText(block.content)}
          </p>
        )
    }
  })
}

export default function CleanSummaryReader({ section, sectionIndex = 0, terms = [], colorMode = true, onWordClick }) {
  const [openSteps, setOpenSteps] = useState(() => new Set([0]))
  useEffect(() => {
    setOpenSteps(new Set([0]))
  }, [sectionIndex, section?.title])

  const toggleStep = index => {
    setOpenSteps(prev => {
      const next = new Set(prev)
      if (next.has(index)) next.delete(index)
      else next.add(index)
      return next
    })
  }

  const rawTakeaways = section.key_takeaways?.length
    ? section.key_takeaways
    : (section.takeaways?.length ? section.takeaways : (section.principles?.length ? section.principles : (section.key_principles || [])))
  let keyIdeas = parseKeyTakeaways(rawTakeaways)
  const topics = (section.subtopics || []).map(topic => ({ ...topic, title: capitalizeSentenceStarts(topic.title), body: capitalizeSentenceStarts(topic.body) }))
  const details = (section.mechanical_deep_dive || []).map(item => ({ ...item, subheading: capitalizeSentenceStarts(item.subheading), body: capitalizeSentenceStarts(item.body) }))
  const paragraphs = (section.body || []).filter(Boolean).map(capitalizeSentenceStarts)
  const overview = capitalizeSentenceStarts(section.foundational_overview || paragraphs[0] || section.subtitle || 'The source pages did not provide enough readable text for an overview.')

  if (!keyIdeas.length) {
    const candidateSentences = [
      ...(overview ? overview.split(/(?<=[.!?])\s+/) : []),
      ...(paragraphs || []),
      ...(topics.flatMap(t => String(t.body || '').split(/(?<=[.!?])\s+/)) || []),
      ...(details.flatMap(d => String(d.body || '').split(/(?<=[.!?])\s+/)) || [])
    ]
    const extracted = []
    for (const sentence of candidateSentences) {
      const clean = String(sentence || '').trim()
      if (clean.length >= 22 && !extracted.some(item => item.toLowerCase().slice(0, 30) === clean.toLowerCase().slice(0, 30))) {
        extracted.push(clean)
        if (extracted.length >= 4) break
      }
    }
    keyIdeas = parseKeyTakeaways(extracted)
  }

  const title = conciseDocumentHeading(section.title, keyIdeas)
  const subtitle = capitalizeSentenceStarts(section.subtitle)
  const visibleFlowSteps = buildFlowStages(section, keyIdeas, topics, details, paragraphs, overview)
  const significanceSources = [overview, ...paragraphs, ...keyIdeas, ...topics.map(topic => topic.body), ...details.map(item => item.body)]
  const practicalExamples = [...new Set(significanceSources.flatMap(value => String(value || '').split(/(?<=[.!?])\s+/)))]
    .filter(sentence => /\b(?:examples?|such as|for instance|used in|used for|application|in practice|industry|clinical|medical|benefit)\b/i.test(sentence))
  const savedSignificance = section.clinical_or_realworld_significance || ''
  const significance = savedSignificance && !/the source (?:does not|did not) (?:state|provide)/i.test(savedSignificance)
    ? capitalizeSentenceStarts(savedSignificance)
    : practicalExamples.length
    ? `The source connects these ideas to practical examples: ${practicalExamples.slice(0, 2).join(' ')}`
    : 'These pages explain the topic, but do not include a specific practical example.'
  const moduleSummaryPoints = (() => {
    const points = []
    if (keyIdeas && keyIdeas.length > 0) {
      keyIdeas.forEach(idea => {
        const clean = idea.trim()
        if (clean && !points.includes(clean)) points.push(clean)
      })
    }
    if (overview && overview.trim()) {
      const sentences = overview.split(/(?<=[.!?])\s+/).filter(s => s.trim().length > 15)
      sentences.slice(0, 2).forEach(s => {
        const clean = s.trim()
        if (clean && !points.some(p => p.toLowerCase().includes(clean.toLowerCase().slice(0, 30)))) {
          points.push(clean)
        }
      })
    }
    if (topics && topics.length > 0) {
      topics.forEach(t => {
        const lead = (t.body || '').split(/(?<=[.!?])\s+/)[0]?.trim()
        if (lead && lead.length > 15 && !points.some(p => p.toLowerCase().includes(lead.toLowerCase().slice(0, 30)))) {
          points.push(lead)
        }
      })
    }
    if (significance && !significance.toLowerCase().includes('not include a specific practical')) {
      const firstSig = significance.split(/(?<=[.!?])\s+/)[0]?.trim()
      if (firstSig && !points.some(p => p.toLowerCase().includes(firstSig.toLowerCase().slice(0, 30)))) {
        points.push(firstSig)
      }
    }
    return points.slice(0, 6).map(capitalizeSentenceStarts)
  })()
  
  const seenTerms = new Set()
  const renderText = (value, customSeen) => highlightDocumentText(value, terms, colorMode, onWordClick, customSeen || new Set())

  return (
    <div className="comprehensive-reader clean-summary-reader">
      <header className="comprehensive-header">
        <div className="comprehensive-meta">
          <span className="module-badge">MODULE {String(sectionIndex + 1).padStart(2, '0')}</span>
        </div>
        <h1>{title}</h1>
        {subtitle && <p className="document-subtitle">{subtitle}</p>}
      </header>

      <section className="summary-block summary-overview">
        <div className="summary-block-heading"><Lightbulb size={18} /><h2>Foundational overview</h2></div>
        {renderDocumentContent(overview, renderText)}
      </section>

      <section className="summary-block summary-principles">
        <div className="summary-block-heading"><BookOpen size={18} /><h2>Key principles & discoveries</h2></div>
        {keyIdeas.length
          ? <div className="principles-grid">
              {keyIdeas.map((idea, index) => (
                <div key={`${idea}-${index}`} className="principle-card">
                  <span className="principle-index">{String(index + 1).padStart(2, '0')}</span>
                  <p className="principle-body document-paragraph-short">{renderText(idea)}</p>
                </div>
              ))}
            </div>
          : <p className="summary-unavailable">No distinct principles could be extracted from these pages.</p>}
      </section>

      <section className="summary-block summary-content">
        <div className="summary-block-heading"><h2>Technical deep dive & mechanics</h2></div>
        {topics.length
          ? topics.map((topic, index) => (
            <article className="summary-topic" key={`${topic.title}-${index}`}>
              {topic.title && <h3>{topic.title}</h3>}
              {renderDocumentContent(topic.body, renderText)}
            </article>
          ))
          : details.length
            ? details.map((item, index) => (
              <article className="summary-topic" key={`${item.subheading}-${index}`}>
                <h3>{item.subheading}</h3>
                {renderDocumentContent(item.body, renderText)}
              </article>
            ))
            : paragraphs.length
              ? renderDocumentContent(paragraphs, renderText)
              : <p className="summary-unavailable">No further readable explanation was found in these pages.</p>}
      </section>

      <section className="summary-block summary-flowchart">
        <div className="summary-block-heading"><GitBranch size={18} /><h2>Concept flowchart</h2></div>
        {visibleFlowSteps.length > 0
          ? <ol className="flowchart-list" aria-label={`Document flowchart for ${title}`}>
            {visibleFlowSteps.map((step, index) => (
              <li key={`${step.title}-${index}`} className="flowchart-item">
                <button
                  type="button"
                  className={`flowchart-node-button ${openSteps.has(index) ? 'is-open' : ''}`}
                  onClick={() => toggleStep(index)}
                  aria-expanded={openSteps.has(index)}
                >
                  <div className="flowchart-card-header">
                    <span className="flowchart-number">{String(index + 1).padStart(2, '0')}</span>
                    <strong className="flowchart-title">{step.title}</strong>
                  </div>
                  <span className="flowchart-hint">{openSteps.has(index) ? 'Hide details ▴' : 'View details ▾'}</span>
                </button>
                {openSteps.has(index) && (
                  <div className="flowchart-detail">
                    {renderDocumentContent(step.description, renderText)}
                  </div>
                )}
                {index < visibleFlowSteps.length - 1 && (
                  <div className="flowchart-connector-wrap" aria-hidden="true">
                    <span className="flowchart-connector">↓</span>
                  </div>
                )}
              </li>
            ))}
          </ol>
          : <p className="summary-unavailable">No connected ideas could be arranged into a flowchart for these pages.</p>}
      </section>

      <section className="summary-block summary-context">
        <div className="summary-block-heading"><h2>Why it matters in practice</h2></div>
        {renderDocumentContent(significance, renderText)}
      </section>

      <section className="summary-block summary-review">
        <div className="summary-block-heading"><ListChecks size={18} /><h2>Module key summary</h2></div>
        {moduleSummaryPoints.length > 0 ? (
          <ul className="module-summary-points">
            {moduleSummaryPoints.map((point, index) => (
              <li key={index} className="module-summary-point-item">
                <span className="module-point-bullet">{String(index + 1).padStart(2, '0')}</span>
                <p className="module-point-text document-paragraph-short">{renderText(point)}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="summary-unavailable">No summary points available for this module.</p>
        )}
      </section>
    </div>
  )
}
