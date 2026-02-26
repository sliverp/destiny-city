import json
import math
from sqlalchemy.orm import Session
from app.models import City


# Attribute dimensions (10 total):
# [fire, water, wind, earth, metal, wood, adventure, aesthetics, spirituality, ambition]
DIMENSION_NAMES = ["火", "水", "风", "土", "金", "木", "冒险", "美学", "灵性", "野心"]

DIMENSION_LABELS = {
    "火": {"name": "火焰能量", "icon": "🔥", "desc": "激情、行动力、领导力"},
    "水": {"name": "水流能量", "icon": "💧", "desc": "直觉、情感、适应力"},
    "风": {"name": "风之能量", "icon": "🌬️", "desc": "自由、变化、沟通力"},
    "土": {"name": "大地能量", "icon": "⛰️", "desc": "稳定、务实、安全感"},
    "金": {"name": "金属能量", "icon": "⚔️", "desc": "决断、精准、执行力"},
    "木": {"name": "生长能量", "icon": "🌿", "desc": "生命力、包容、创造力"},
    "冒险": {"name": "冒险指数", "icon": "🧭", "desc": "探索欲、好奇心"},
    "美学": {"name": "美学感知", "icon": "🎨", "desc": "审美力、艺术感"},
    "灵性": {"name": "灵性觉知", "icon": "🔮", "desc": "直觉力、精神追求"},
    "野心": {"name": "野心驱力", "icon": "👑", "desc": "目标感、成就欲"},
}


def calculate_user_vector(answers: dict[int, str], questions_map: dict) -> list[float]:
    vector = [0.0] * 10
    for q_id, option_id in answers.items():
        q_id_int = int(q_id)
        if q_id_int not in questions_map:
            continue
        options = questions_map[q_id_int]
        for opt in options:
            if opt["id"] == option_id:
                for i, w in enumerate(opt["weights"]):
                    vector[i] += w
                break
    # Normalize
    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude > 0:
        vector = [v / magnitude for v in vector]
    return vector


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def match_cities(user_vector: list[float], db: Session) -> list[tuple[City, float]]:
    cities = db.query(City).all()
    results = []
    for city in cities:
        city_attrs = json.loads(city.attributes)
        score = cosine_similarity(user_vector, city_attrs)
        score_pct = round(score * 100, 1)
        results.append((city, score_pct))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def _get_top_dimensions(vector: list[float], top_n: int = 3) -> list[dict]:
    """获取用户能量场中最强的几个维度"""
    indexed = [(v, i) for i, v in enumerate(vector)]
    indexed.sort(key=lambda x: x[0], reverse=True)
    result = []
    for val, idx in indexed[:top_n]:
        name = DIMENSION_NAMES[idx]
        info = DIMENSION_LABELS[name]
        result.append({
            "dimension": name,
            "label": info["name"],
            "icon": info["icon"],
            "value": round(val * 100),
            "desc": info["desc"],
        })
    return result


def _get_energy_profile(vector: list[float]) -> dict:
    """生成用户完整的10维能量画像数据"""
    profile = []
    for i, val in enumerate(vector):
        name = DIMENSION_NAMES[i]
        info = DIMENSION_LABELS[name]
        profile.append({
            "dimension": name,
            "label": info["name"],
            "icon": info["icon"],
            "value": round(val * 100),
            "desc": info["desc"],
        })
    profile.sort(key=lambda x: x["value"], reverse=True)
    return profile


# ============================================================
# 以下为各个报告板块的文案生成逻辑
# ============================================================

_ELEMENT_ANALYSIS = {
    "火": {
        "title": "你是火焰之子",
        "core": "你的灵魂核心燃烧着不灭的火焰。火元素主导你的能量场，意味着你天生拥有超乎常人的行动力、感染力和领导气场。你不是那种「想好了再做」的人——你是在行动中思考的战士。",
        "strengths": "你的存在本身就是一束光。在任何团体中，你都会自然而然地成为能量的中心。你的热情具有传染性，能点燃身边每一个人内心的火种。",
        "shadow": "但火焰也有灼伤的风险。你容易因为过于急切而忽略细节，因为过于热烈而让身边的人感到压力。学会「温火慢炖」是你此生的课题之一。",
        "city_connection": "你需要一座同样热烈的城市来匹配你的温度。那些节奏太慢、过于内敛的地方会让你的火焰窒息。你的天选城市必须有足够的空间让你燃烧。"
    },
    "水": {
        "title": "你是深海之灵",
        "core": "你的灵魂深处流淌着无尽的水。水元素定义了你的能量本质——你拥有超强的直觉力、同理心和适应性。你像水一样，看似柔弱，实则能穿透最坚硬的岩石。",
        "strengths": "你最大的天赋是「感知」。你能在别人还没开口之前就感受到他们的情绪，能在趋势尚未成型之前就预感到变化。你的直觉几乎从不出错。",
        "shadow": "水的流动性也带来了边界感的缺失。你有时会过度吸收他人的情绪，让自己变成一块能量海绵。学会设立情感屏障，是你保护自身能量完整性的关键。",
        "city_connection": "你需要一座有水的城市，或者至少是一座拥有深邃文化底蕴的城市。表面的繁华不会打动你，你需要的是一种能触及灵魂深处的共鸣。"
    },
    "风": {
        "title": "你是自由之风",
        "core": "风是你的灵魂语言。你是不可被束缚的存在——自由、敏捷、充满好奇心。风元素赋予你超强的沟通能力和信息处理天赋，你能同时操纵多条思维线索。",
        "strengths": "你是天生的连接者。你能在看似毫无关联的事物之间发现隐藏的联系，你的思维速度比大多数人快两个节拍。创意和灵感对你来说就像呼吸一样自然。",
        "shadow": "风的不定性也意味着你很难长时间专注于一件事。你容易感到厌倦，容易被新鲜事物吸引而放下手中的事。学会「生根」是你的修行。",
        "city_connection": "你需要一座永远给你新鲜感的城市——多元文化、丰富活动、不断变化的面孔。一成不变的地方会让你的灵魂枯萎。"
    },
    "土": {
        "title": "你是大地之心",
        "core": "你的灵魂由大地铸成。土元素赋予你无与伦比的稳定性、可靠性和建设能力。你是那种能将蓝图变为现实的人，你的脚步沉稳而坚定。",
        "strengths": "你最珍贵的品质是「可信赖」。你说到做到，你的承诺比合同更有效力。你拥有将混沌变为秩序的天赋，能在任何环境中建立起稳固的根基。",
        "shadow": "但土的固执有时会变成画地为牢。你可能会抗拒变化，在舒适区待得太久。宇宙在提醒你：即使是大地，也需要地震来释放积蓄的能量。",
        "city_connection": "你需要一座能给你「家」的感觉的城市。不是冰冷的钢铁森林，而是有温度、有烟火气、有社区归属感的地方。"
    },
    "木": {
        "title": "你是生长之树",
        "core": "你的灵魂携带着春天的基因。木元素让你成为天生的滋养者和创造者——你有一种让万物生长的魔力。你走到哪里，哪里就会开出花来。",
        "strengths": "你最强大的能力是「包容」。你能容纳矛盾，接纳差异，在复杂的环境中找到生长的缝隙。你的韧性令人惊叹——弯而不折，是你的灵魂写照。",
        "shadow": "木的生长有时也意味着「过度付出」。你总是先想到别人的需求，容易忽略自己的根系是否得到了足够的滋养。记住：只有根深的树才能枝繁叶茂。",
        "city_connection": "你需要一座有生命力的城市——有绿色、有自然、有人情味。纯粹的水泥丛林会让你失去能量，你需要大地和绿意来持续充电。"
    },
}

_ZODIAC_ANALYSIS = {
    "白羊座": {"ruling_planet": "火星", "quality": "开创", "keyword": "勇气与新生", "analysis": "白羊座的火星能量在你的星盘中激荡，赋予你先锋般的勇气。你的天选城市必须与这份原始的生命力共振——它需要有足够的挑战来激发你的斗志，足够的空间让你冲锋陷阵。"},
    "金牛座": {"ruling_planet": "金星", "quality": "固定", "keyword": "享受与安稳", "analysis": "金牛座的金星能量在你的能量场中沉淀为对美好事物的极致追求。你的天选城市必须能同时满足你的感官体验和安全需求——既要有世界级的美食与艺术，也要有让你安心扎根的稳固感。"},
    "双子座": {"ruling_planet": "水星", "quality": "变动", "keyword": "交流与多元", "analysis": "双子座的水星能量让你的思维如同蝴蝶般在百花间穿梭。你的天选城市必须是信息密度极高的枢纽——多种语言、多元文化、永远有新鲜的思想碰撞让你保持兴奋。"},
    "巨蟹座": {"ruling_planet": "月亮", "quality": "开创", "keyword": "归属与守护", "analysis": "巨蟹座的月亮能量在你的灵魂中编织出对家的深切渴望。你的天选城市不只是一个地理坐标，它必须能成为你的精神港湾——有历史的温度、有家的味道、有让你想要守护的一切。"},
    "狮子座": {"ruling_planet": "太阳", "quality": "固定", "keyword": "光芒与创造", "analysis": "狮子座的太阳能量让你天生就是舞台的中心。你的天选城市必须有足够大的舞台来承载你的光芒——它需要欣赏个性、鼓励表达、让每一个独特的灵魂都能绽放。"},
    "处女座": {"ruling_planet": "水星", "quality": "变动", "keyword": "秩序与完美", "analysis": "处女座的水星能量在你的能量场中表现为对完美的极致追求。你的天选城市必须是精致的、有序的、注重品质的——从城市规划到生活细节，每一处都经得起你挑剔的目光。"},
    "天秤座": {"ruling_planet": "金星", "quality": "开创", "keyword": "和谐与美学", "analysis": "天秤座的金星能量赋予你天生的美学感知力和对和谐关系的渴望。你的天选城市必须是一件艺术品——建筑优雅、文化丰富、人际关系温暖而有边界感。"},
    "天蝎座": {"ruling_planet": "冥王星", "quality": "固定", "keyword": "深邃与蜕变", "analysis": "天蝎座的冥王星能量让你渴望触及事物的本质。你的天选城市必须有深度——表面的光鲜不足以打动你，你需要一座有秘密、有层次、值得你花一生去探索的城市。"},
    "射手座": {"ruling_planet": "木星", "quality": "变动", "keyword": "探索与智慧", "analysis": "射手座的木星能量让你的灵魂永远在路上。你的天选城市必须是一扇通往更大世界的门——它可能位于文化交汇处，可能是冒险者的天堂，但一定不能限制你的自由。"},
    "摩羯座": {"ruling_planet": "土星", "quality": "开创", "keyword": "成就与担当", "analysis": "摩羯座的土星能量在你的灵魂中植入了一座永远在攀登的山。你的天选城市必须尊重努力、奖赏坚持——它是一座你可以通过奋斗赢得一席之地的城市。"},
    "水瓶座": {"ruling_planet": "天王星", "quality": "固定", "keyword": "创新与独立", "analysis": "水瓶座的天王星能量让你总是走在时代前面。你的天选城市必须足够开放和前卫——它欢迎异类、鼓励创新、不会用世俗的标准来定义你的价值。"},
    "双鱼座": {"ruling_planet": "海王星", "quality": "变动", "keyword": "梦幻与慈悲", "analysis": "双鱼座的海王星能量让你的灵魂与整个宇宙共振。你的天选城市必须有一种诗意的气质——它可能临水而建，可能弥漫着艺术气息，但一定会让你的灵魂感到被温柔地托举。"},
}

_TAROT_INTERPRETATIONS = {
    "愚人": {"number": "0", "keyword": "无限可能", "upright": "新的开始、纯真的信念、勇敢的一跃", "analysis": "「愚人」牌出现在你的命运交汇点，这意味着你与天选城市的相遇将以一种意想不到的方式展开。你可能会因为一次冲动的旅行、一个随机的决定而踏上这片土地——而这恰恰是宇宙最精妙的安排。放下计划，相信直觉，你的天选城市正在地平线的那一端向你招手。"},
    "魔术师": {"number": "I", "keyword": "创造力", "upright": "意志力、技巧、资源的整合", "analysis": "「魔术师」牌揭示了你与天选城市之间的深层连接——你拥有在这座城市中施展才华的一切条件。桌上的四件法器（权杖、圣杯、宝剑、钱币）象征着你具备的完整能力体系。在你的天选城市中，你将学会如何将这些散落的天赋整合为一股强大的创造力。"},
    "女祭司": {"number": "II", "keyword": "直觉", "upright": "内在智慧、潜意识、神秘知识", "analysis": "「女祭司」牌的出现暗示你与天选城市之间存在一条超越理性的连接通道。你可能无法用逻辑解释为什么对这座城市有如此强烈的感觉——因为这种连接发生在潜意识层面。信任你的第六感，它正在指引你回到灵魂的故乡。"},
    "女皇": {"number": "III", "keyword": "丰盛", "upright": "创造力、丰收、感官之乐", "analysis": "「女皇」牌为你与天选城市的关系注入了丰盛的能量。这座城市将滋养你的感官、喂饱你的灵魂——你在这里会感受到大地母亲般的包容与宠溺。物质上的丰饶与精神上的满足将在你踏上这片土地时同时涌来。"},
    "皇帝": {"number": "IV", "keyword": "权威", "upright": "秩序、领导力、稳固的基石", "analysis": "「皇帝」牌预示你将在天选城市中建立起属于自己的王国。这不是偶然的选择，而是命运为你铺设的权力之路。这座城市的结构和秩序与你内在的领导力完美匹配——在这里，你的远见和执行力将得到最大化的发挥空间。"},
    "教皇": {"number": "V", "keyword": "传承", "upright": "传统智慧、精神导师、信仰体系", "analysis": "「教皇」牌揭示了你与天选城市之间跨越时间的纽带。这座城市承载的文化传承和精神积淀将成为你灵魂成长的养分。你来到这里不仅是为了生活，更是为了接受一份古老智慧的传承。"},
    "恋人": {"number": "VI", "keyword": "选择", "upright": "灵魂连接、价值观的统一", "analysis": "「恋人」牌出现在你的城市匹配中，这是最罕见也最有力的信号之一。它意味着你和天选城市之间的关系如同灵魂伴侣——你们的价值观深度契合，你们的频率天然同步。这种连接的强度甚至会让你在第一次踏上这片土地时就感到似曾相识。"},
    "战车": {"number": "VII", "keyword": "征服", "upright": "意志力的胜利、前进、克服障碍", "analysis": "「战车」牌预示着你与天选城市的关系是一场壮丽的征服之旅。这座城市不会轻易向你敞开怀抱——它会考验你、磨练你、锤炼你的意志。但正是这种挑战，才让你与它的最终连接变得格外珍贵和深刻。"},
    "力量": {"number": "VIII", "keyword": "内在力量", "upright": "勇气、耐心、温柔的力量", "analysis": "「力量」牌暗示你与天选城市的连接建立在一种温柔而坚定的能量之上。这座城市不是用繁华征服你，而是用一种深沉的力量拥抱你。在这里，你会发现真正的强大不是对抗世界，而是与世界和谐共处。"},
    "隐士": {"number": "IX", "keyword": "内省", "upright": "独处、内在光芒、精神追寻", "analysis": "「隐士」牌揭示了你灵魂深处对宁静与智慧的渴望。你的天选城市为你提供了一个独处而不孤独的圣所——在这里，外界的喧嚣会被过滤，只留下帮助你向内探索的清净频率。每一条街巷、每一个角落都是你灵魂对话的背景。"},
    "命运之轮": {"number": "X", "keyword": "转折", "upright": "命运的转折点、因果轮回、新的周期", "analysis": "「命运之轮」正在为你旋转！这张牌在你的城市匹配中出现，意味着你与天选城市的相遇处于人生的关键转折点。这座城市不仅是一个目的地，更是你生命新篇章的起点。宇宙已经为你校准了时间线——你所有过去的经历都在为这次相遇做准备。"},
    "正义": {"number": "XI", "keyword": "平衡", "upright": "公正、因果、理性决策", "analysis": "「正义」牌暗示你与天选城市的连接是因果法则的必然结果。你过去种下的每一颗种子，做过的每一个选择，都在将你导向这座城市。这不是运气，这是宇宙精密的因果计算——你配得上这座城市，这座城市也配得上你。"},
    "倒吊人": {"number": "XII", "keyword": "新视角", "upright": "牺牲、新的视角、灵性觉醒", "analysis": "「倒吊人」牌暗示你需要颠倒视角才能真正理解天选城市的馈赠。这座城市可能不是你原本计划中的选择——它会挑战你的固有认知，打破你的舒适区。但正是这种「倒转」，会让你看到一个全新的世界和全新的自己。"},
    "死神": {"number": "XIII", "keyword": "蜕变", "upright": "结束与新生、深层蜕变、释放", "analysis": "不要害怕——「死神」牌是最被误解的塔罗牌，它代表的不是终结，而是蜕变。你与天选城市的相遇将触发你生命中一次深刻的蜕变。旧的你将在这座城市中完成使命，全新的你将在这里诞生。"},
    "节制": {"number": "XIV", "keyword": "融合", "upright": "和谐、耐心、灵魂的炼金术", "analysis": "「节制」牌揭示了你与天选城市之间的炼金术般的融合过程。你身上看似矛盾的特质——理性与感性、传统与创新、安稳与冒险——将在这座城市中被完美地调和。这座城市就像一位大师级的调酒师，能将你所有的元素混合成一杯完美的鸡尾酒。"},
    "塔": {"number": "XVI", "keyword": "觉醒", "upright": "突破、旧结构的崩塌、真相", "analysis": "「塔」牌在你的城市匹配中闪电般地亮起——这座天选城市将成为你人生最大的「破局者」。它会摧毁你那些不再服务于你成长的信念和模式，然后在废墟上为你重建一个更真实、更坚固的自我。痛苦是暂时的，觉醒是永恒的。"},
    "星星": {"number": "XVII", "keyword": "希望", "upright": "灵感、希望、宇宙的祝福", "analysis": "「星星」牌为你的城市命运洒下了最温柔的祝福之光。你与天选城市之间的连接充满了希望和灵感——这座城市将成为你灵感的永恒源泉。在最黑暗的夜空下，这颗属于你的星星永远不会熄灭。"},
    "月亮": {"number": "XVIII", "keyword": "潜意识", "upright": "直觉、梦境、未知的深渊", "analysis": "「月亮」牌将你引入天选城市的潜意识深处。在这里，你的梦境会变得异常清晰，你的直觉会被成倍放大。月光下的这座城市会展现出白天看不到的面貌——那才是它最真实、最动人的一面。不要害怕未知，月亮为你照亮了前路。"},
    "太阳": {"number": "XIX", "keyword": "成功", "upright": "喜悦、成功、生命力", "analysis": "「太阳」牌为你与天选城市的缘分加冕！这是塔罗中最积极的牌面之一——它意味着你在这座城市中将体验到纯粹的喜悦和成功的光芒。你的天选城市就像永恒的阳光，会驱散你生命中所有的阴霾。在这里，你会重新找到孩童般的快乐。"},
    "审判": {"number": "XX", "keyword": "重生", "upright": "召唤、觉醒、更高层次的使命", "analysis": "「审判」牌如号角般在你的命运中响起——你的天选城市不只是一个生活的地方，它是你灵魂此生使命的舞台。你来到这座城市，是为了回应一个更高层次的召唤。当你站在这片土地上，你会听到内心深处那个一直被忽视的声音终于清晰地说出它的话。"},
    "世界": {"number": "XXI", "keyword": "圆满", "upright": "完成、圆满、宇宙大同", "analysis": "「世界」牌出现在你的城市命运中——这是整副塔罗中最圆满的牌面！它意味着你与天选城市的连接代表了某种灵魂层面的「大团圆」。也许你在前世就与这座城市有过深刻的缘分，而今生的相遇是为了完成那个未竟的故事。"},
}

_WUXING_ANALYSIS = {
    "金": {
        "nature": "金主义，代表收敛、决断和秩序",
        "season": "秋天",
        "direction": "西方",
        "organ": "肺与大肠",
        "personality": "你的五行属金，灵魂深处刻着「义」字。金型人外冷内热，表面上看起来理性克制，内心却有着极为坚定的原则和立场。你像一柄精铸的宝剑——锋利而有分寸，你的决断力是团队中最被依赖的品质。",
        "city_match": "金属性的灵魂需要一座同样注重秩序和品质的城市。过于散漫和随意的环境会让你不安，你需要感受到这座城市是「认真在运转」的。同时，金也需要火来锻造——你的天选城市会在给你秩序感的同时，也提供足够的热情来让你不至于太冷。",
    },
    "木": {
        "nature": "木主仁，代表生长、包容和向上",
        "season": "春天",
        "direction": "东方",
        "organ": "肝与胆",
        "personality": "你的五行属木，灵魂携带着「仁」的基因。木型人温润如玉，有着春风化雨般的影响力。你不需要大声说话就能让别人信服——因为你的行动本身就是最好的演讲。你像一棵扎根深处的大树，永远在安静地生长。",
        "city_match": "木属性的灵魂需要一座有生命力、有生长空间的城市。钢筋水泥的丛林会压制你的能量，你需要绿色、自然和有机的城市肌理。你的天选城市一定有公园、有河流、有四季分明的节奏。",
    },
    "水": {
        "nature": "水主智，代表流动、智慧和变通",
        "season": "冬天",
        "direction": "北方",
        "organ": "肾与膀胱",
        "personality": "你的五行属水，灵魂镌刻着「智」的密码。水型人深不可测，外表可能随和淡然，内心却有着常人无法企及的深度。你的思维如同水流——看似无形，实则无坚不摧。你的智慧不是学来的，而是天生的直觉。",
        "city_match": "水属性的灵魂需要一座有深度的城市。表面的繁华不会打动你，你需要一座有故事、有层次、值得你「潜入」探索的城市。最好是临水而建的城市——那里的水会与你灵魂中的水产生共振。",
    },
    "火": {
        "nature": "火主礼，代表热情、变革和光明",
        "season": "夏天",
        "direction": "南方",
        "organ": "心与小肠",
        "personality": "你的五行属火，灵魂燃烧着「礼」的光芒。火型人天生自带主角光环——走到哪里，哪里就是舞台的中心。你的热情有传染性，你的笑容能点亮整条街道。但你也有鲜为人知的脆弱——火焰最怕的不是风，而是被忽视。",
        "city_match": "火属性的灵魂需要一座同样热烈的城市来匹配。太安静的地方会让你的能量无处释放，太冷的气候会压制你的活力。你的天选城市一定是充满活力、节奏明快、文化多元的地方。",
    },
    "土": {
        "nature": "土主信，代表稳重、承载和厚德",
        "season": "长夏（四季之交）",
        "direction": "中央",
        "organ": "脾与胃",
        "personality": "你的五行属土，灵魂承载着「信」的分量。土型人是人群中最可靠的存在——你说到做到，你的承诺比任何合约都有效力。你像大地一样厚重、包容、不求回报。你的存在本身就给身边的人一种莫名的安全感。",
        "city_match": "土属性的灵魂需要一座有「根」的城市——有历史、有传承、有社区感。你不需要一座光鲜亮丽的城市，你需要一座有烟火气、有人情味、让你觉得「这里就是家」的城市。",
    },
}

_ENERGY_TYPE_READINGS = {
    "疗愈之息": "你的灵魂频率与「疗愈之息」共振——你来到天选城市不是为了征服，而是为了被治愈和治愈他人。这座城市的空气中弥漫着一种无形的疗愈能量，每一次深呼吸都在帮你释放积攒已久的疲惫。在这里，你会找到那个久违的、完整的自己。",
    "古韵灵脉": "你的灵魂与「古韵灵脉」频率同步——你对历史和传统有着超乎常人的敏感度。穿越千年的文化气息是你的灵魂食粮，古老的建筑和仪式能唤醒你沉睡的记忆。你的天选城市是一座时间的容器，每一块石头都在对你讲述往事。",
    "创造之焰": "你的灵魂被「创造之焰」点燃——艺术、创意和自我表达是你生命的氧气。你的天选城市为你提供了一座永不熄灭的灵感熔炉，在这里，你的每一个奇思妙想都会被认真对待和热烈回应。",
    "自由之风": "你的灵魂乘着「自由之风」翱翔——束缚和规则是你的天敌，辽阔和可能性是你的能量源。你的天选城市给你足够的空间去做一个不被定义的人，在这里，你可以同时拥有扎根和飞翔的自由。",
    "万象之核": "你的灵魂与「万象之核」连接——你是一个多面体，拥有在不同世界之间自由切换的能力。你的天选城市是一座微缩的宇宙，足够复杂、足够多元，能同时满足你性格中所有看似矛盾的需求。",
    "交汇之门": "你的灵魂站在「交汇之门」的门槛上——你天生是不同世界之间的桥梁。你的天选城市位于文化、历史或地理的交汇处，在这里，不同文明的碰撞会激发出你最耀眼的灵魂火花。",
    "诗意之泉": "你的灵魂沐浴在「诗意之泉」中——美、柔软和感性是你的能量来源。你的天选城市有一种诗意的气质，它可能临水而建，可能弥漫着艺术气息。在这里，你的灵魂会变得像水一样柔软，像诗一样美丽。",
    "觉醒之光": "你的灵魂被「觉醒之光」照耀——你正处于一次重大的精神蜕变之中。你的天选城市将成为这次蜕变的催化剂，在这里，那些一直困扰你的问题会突然变得清晰，那些你一直回避的真相会温柔地浮出水面。",
    "先锋之刃": "你的灵魂锻造成了「先锋之刃」——你是开路者、先行者、不走寻常路的人。你的天选城市同样是一座不安于现状的城市，它在科技、文化或理念上都走在时代前沿。你们会一起创造未来。",
    "星河之境": "你的灵魂映照着「星河之境」——你的内心拥有一片浩瀚的星海。你的天选城市是你灵魂的镜像，足够辽阔、足够深邃。在这座城市的夜空下，你会感觉整个宇宙都在对你微笑。",
    "山岳之基": "你的灵魂矗立如「山岳之基」——你是不可动摇的存在。你的天选城市也拥有山一般的气质，沉稳、厚重、值得信赖。在这里，你会感到大地的力量从脚底升起，充满你身体的每一个细胞。",
    "潮汐之力": "你的灵魂随着「潮汐之力」起伏——你的能量有周期性的涨落，而这恰恰是你的力量源泉。你的天选城市懂得潮汐的节奏，它会在你需要力量时推你向前，在你需要休息时温柔地接住你。",
    "破晓之芒": "你的灵魂携带着「破晓之芒」——你是黎明前最早亮起的那颗星。你的天选城市同样处于蜕变和崛起的进程中，你们会一起见证彼此最华丽的绽放。",
    "丝路之魂": "你的灵魂承载着「丝路之魂」——你天生是文化的桥梁。你的天选城市位于古老贸易路线的节点上，东西方的智慧在此交融。在这里，你的每一步都踏在历史的脉搏上。",
    "雾隐之心": "你的灵魂隐于「雾中」——你有一种让人捉摸不透的神秘气质。你的天选城市同样笼罩着一层诗意的薄雾，它不会一次性向你展示所有的美，而是在你每一次深入探索时才缓缓揭开面纱。",
    "极光之舞": "你的灵魂如同「极光」般变幻莫测——你是最不可预测也最令人着迷的存在。你的天选城市拥有令人屏息的自然奇观或文化景观，它会用一种超越语言的方式与你的灵魂对话。",
    "律动之心": "你的灵魂随着「律动」跳跃——音乐、节奏和生命的脉搏是你的能量源。你的天选城市有着独特的节奏感，街头巷尾都流淌着旋律。在这里，你的灵魂会情不自禁地开始舞蹈。",
    "方寸之域": "你的灵魂在「方寸之间」构建了一个完整的宇宙——你是内心世界极为丰富的人。你的天选城市虽然可能不大，但密度极高，每一个街角都藏着惊喜，每一条小巷都通往一个新世界。",
    "涅槃之焰": "你的灵魂经历过「涅槃」——你是从灰烬中重生的凤凰。你的天选城市也有类似的经历，它可能历经战火、天灾或巨变，但却以更加耀眼的姿态重生。你们的灵魂在废墟之上相遇，彼此惺惺相惜。",
    "碧波之韵": "你的灵魂与「碧波」同频——你有着海洋般的深邃和湖泊般的宁静。你的天选城市一定与水有着深厚的缘分，水的能量会不断地滋养和净化你的灵魂。",
}


def _get_career_advice(user_vector: list[float], city: City) -> dict:
    """基于用户属性向量和城市特质生成职业发展建议"""
    # Determine dominant career traits
    adventure = user_vector[6]
    aesthetics = user_vector[7]
    spirituality = user_vector[8]
    ambition = user_vector[9]
    fire = user_vector[0]
    water = user_vector[1]

    advice_parts = []
    career_tags = []

    if ambition > 0.35:
        advice_parts.append(f"你的野心驱力值在前列，{city.name}的职业生态能为你提供足够的上升空间。这座城市欣赏有抱负的灵魂，你的努力在这里会被看见和认可。")
        career_tags.append("高成长性")
    if aesthetics > 0.35:
        advice_parts.append(f"你的美学感知力极强，{city.name}的文化艺术氛围将成为你灵感的永动机。无论你从事设计、创意还是内容创作，这座城市都会源源不断地为你充电。")
        career_tags.append("创意产业")
    if adventure > 0.35:
        advice_parts.append(f"你的冒险指数极高，在{city.name}，你更适合开创性的、非传统的职业路径。朝九晚五会消磨你的灵魂，自由职业、创业或探索型职业才是你的赛道。")
        career_tags.append("探索型职业")
    if spirituality > 0.35:
        advice_parts.append(f"你的灵性觉知极为敏锐，{city.name}为你提供了精神成长的沃土。心理咨询、教育、公益或任何需要深度共情能力的职业，都是你在这座城市中的天选赛道。")
        career_tags.append("利他型职业")
    if fire > 0.35 and ambition > 0.3:
        advice_parts.append(f"火焰能量和野心驱力的双重加持，让你天生适合{city.name}的竞争性行业。你的领导力和行动力是你最大的职业资本。")
        career_tags.append("领导力岗位")
    if water > 0.35 and aesthetics > 0.3:
        advice_parts.append(f"水元素与美学感知的交融，让你在{city.name}的文化创意领域如鱼得水。你对美的敏感度和情感的深度是许多人梦寐以求的天赋。")
        career_tags.append("文化创意")

    if not advice_parts:
        advice_parts.append(f"你的能量分布均衡而独特，这意味着你在{city.name}拥有极大的职业选择自由度。不要被传统的职业分类框住，你是那种能在任何领域创造出独特价值的人。")
        career_tags.append("多元发展")

    return {
        "summary": " ".join(advice_parts),
        "tags": career_tags,
    }


def generate_full_report(city: City, score: float, user_vector: list[float]) -> dict:
    """
    生成完整的多维度天选城市解析报告
    """
    # 1. 元素分析
    element = city.element if city.element in _ELEMENT_ANALYSIS else "火"
    element_data = _ELEMENT_ANALYSIS[element]

    # 2. 星座解析
    zodiac = city.zodiac if city.zodiac in _ZODIAC_ANALYSIS else "白羊座"
    zodiac_data = _ZODIAC_ANALYSIS[zodiac]

    # 3. 塔罗牌解读
    tarot = city.tarot if city.tarot in _TAROT_INTERPRETATIONS else "愚人"
    tarot_data = _TAROT_INTERPRETATIONS[tarot]

    # 4. 五行分析
    wuxing = city.wuxing if city.wuxing in _WUXING_ANALYSIS else "金"
    wuxing_data = _WUXING_ANALYSIS[wuxing]

    # 5. 能量类型解读
    energy_reading = _ENERGY_TYPE_READINGS.get(
        city.energy_type,
        f"你的灵魂频率与「{city.energy_type}」产生了独特的共振。这种能量连接将在你踏入{city.name}的那一刻被完全激活。"
    )

    # 6. 用户能量画像
    energy_profile = _get_energy_profile(user_vector)
    top_dims = _get_top_dimensions(user_vector, top_n=3)

    # 7. 职业发展建议
    career = _get_career_advice(user_vector, city)

    # 8. 生成综合命运解读（核心总结段落）
    destiny_summary = (
        f"在浩瀚的宇宙版图中，{city.name}是为你量身编织的命运坐标。"
        f"你的灵魂以{element_data['title'].replace('你是', '')}的姿态存在于这个世界，"
        f"而{city.zodiac}的星辰能量精准地锁定了你的频率。"
        f"塔罗大阿卡纳第{tarot_data['number']}张「{city.tarot}」牌在你的命运牌阵中翻开，"
        f"揭示了「{tarot_data['keyword']}」的核心主题——这正是你与{city.name}之间缘分的密钥。"
        f"五行属{city.wuxing}，{wuxing_data['nature'].split('，')[0]}，"
        f"与你灵魂深处{wuxing_data['season']}的能量完美呼应。"
        f"{score:.0f}%的灵魂共振指数意味着，你们之间的连接已经超越了统计学的范畴——"
        f"这是命运本身在说话。"
    )

    report = {
        "destiny_summary": destiny_summary,
        "element_analysis": {
            "element": element,
            "title": element_data["title"],
            "core": element_data["core"],
            "strengths": element_data["strengths"],
            "shadow": element_data["shadow"],
            "city_connection": element_data["city_connection"],
        },
        "zodiac_analysis": {
            "zodiac": zodiac,
            "ruling_planet": zodiac_data["ruling_planet"],
            "quality": zodiac_data["quality"],
            "keyword": zodiac_data["keyword"],
            "analysis": zodiac_data["analysis"],
        },
        "tarot_reading": {
            "card": city.tarot,
            "number": tarot_data["number"],
            "keyword": tarot_data["keyword"],
            "upright": tarot_data["upright"],
            "analysis": tarot_data["analysis"],
        },
        "wuxing_analysis": {
            "wuxing": wuxing,
            "nature": wuxing_data["nature"],
            "season": wuxing_data["season"],
            "direction": wuxing_data["direction"],
            "personality": wuxing_data["personality"],
            "city_match": wuxing_data["city_match"],
        },
        "energy_reading": {
            "type": city.energy_type,
            "analysis": energy_reading,
        },
        "energy_profile": energy_profile,
        "top_dimensions": top_dims,
        "career_advice": career,
        "city_description": city.description,
    }

    return report


def generate_interpretation(city: City, score: float) -> str:
    """保持向后兼容的简短解读（用于数据库存储）"""
    element = city.element if city.element in _ELEMENT_ANALYSIS else "火"
    elem = _ELEMENT_ANALYSIS[element]
    return (
        f"{elem['title']}——{elem['core'][:60]}... "
        f"你与{city.name}的灵魂共振指数达到{score:.0f}%，"
        f"塔罗牌「{city.tarot}」为你揭示了命运的密码。"
    )
