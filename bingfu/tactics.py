"""
BingFu Framework - 孙子兵法战术引擎
Sun Tzu's Art of War Tactics Engine

基于《孙子兵法》的经典战术实现，
为Agent提供古代军事智慧支持。
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


# ==================== 战术枚举 ====================

class TacticType(Enum):
    """孙子兵法十三篇战术类型"""
    # 始计篇 - 庙算
    RECONNAISSANCE = "知己知彼"           # 知彼知己，百战不殆
    STRATEGIC_PLANNING = "庙算"           # 多算胜，少算不胜

    # 作战篇 - 速战
    RAPID_WARFARE = "兵贵速胜"            # 兵贵胜，不贵久
    RESOURCE_MANAGEMENT = "取用于国"       # 取用于国，因粮于敌

    # 谋攻篇 - 全胜
    TOTAL_VICTORY = "不战而胜"            # 上兵伐谋
    STRATEGIC_ALLIANCE = "联横合纵"       # 其次伐交

    # 军形篇 - 自保
    DEFENSIVE_SUPERIORITY = "先为不可胜"   # 先为不可胜，以待敌之可胜
    TERRAIN_ADVANTAGE = "地生度"          # 地生度，度生量

    # 兵势篇 - 奇正
    REGULAR_VS_SPECIAL = "奇正相生"       # 战势不过奇正，奇正相生
    SURPRISE_ATTACK = "出其不意"          # 凡战者，以正合，以奇胜

    # 虚实篇 - 致人
    CONTROL_ENEMY = "致人而不致于人"       # 善战者，致人而不致于人
    FLEXIBLE_RESPONSE = "因敌而变"        # 兵形象水，水之形避高而趋下

    # 军争篇 - 迁直
    INDIRECT_APPROACH = "迁直之计"         #军争之难者，以迂为直
    MORALE_WINNING = "夺气夺心"           # 三军可夺气，将军可夺心

    # 九变篇 - 变通
    ADAPTABILITY = "变通在地"            # 合于利而动，不合于利而止
    STRATEGIC_FLEXIBILITY = "九变"        # 智者之虑，必杂于利害

    # 行军篇 - 察情
    INTELLIGENCE_GATHERING = "察敌之情"   # 敌近而静者，恃其险也
    TERRAIN_SELECTION = "处军之利"        # 绝山依谷，视生处高

    # 地形篇 - 六地
    TERRAIN_TACTICS = "六地之用"          # 通形、挂形、支形、隘形、险形、远形
    SOLDIER_MANAGEMENT = "兵卒之道"       # 令素行以教其民，则民服

    # 九地篇 - 九变
    NINE_TERRAINS = "九地之变"            # 散地、轻地、争地、交地、衢地
    RAPID_DEPLOYMENT = "并敌一向"         # 顺详敌之意，并敌一向

    # 火攻篇 - 火攻
    FIRE_ATTACK = "火攻有五"             # 火发于火攻有五
    COORDINATED_ATTACK = "五火之变"       # 以火佐攻者明，以水佐攻者强

    # 用间篇 - 用间
    ESPIONAGE = "用间有五"               # 因间、内间、反间、死间、生间
    INTELLIGENCE_NETWORK = "五间俱起"     # 五间俱起，莫知其道


# ==================== 战术上下文 ====================

class TacticalContext(BaseModel):
    """战术执行上下文"""
    self_strength: int = Field(default=0, description="己方兵力")
    enemy_strength: int = Field(default=0, description="敌方兵力")
    terrain: str = Field(default="平原", description="地形")
    weather: str = Field(default="晴", description="天气")
    morale: int = Field(default=50, description="士气(0-100)")
    supplies: int = Field(default=100, description="补给(0-100)")
    time_factor: str = Field(default="白天", description="时间")
    has_intelligence: bool = Field(default=False, description="是否有情报")


# ==================== 战术引擎 ====================

class TacticsEngine:
    """
    孙子兵法战术引擎

    提供基于《孙子兵法》的智能战术建议。
    """

    def __init__(self):
        self.tactics_log: List[Dict[str, Any]] = []

    def analyze(self, context: TacticalContext) -> Dict[str, Any]:
        """
        分析战场态势，返回战术建议

        Args:
            context: 战术上下文

        Returns:
            包含战术建议和建议程度的字典
        """
        # 知己知彼
        intelligence_advice = self._know_enemy(context)

        # 力量对比
        strength_ratio = context.self_strength / max(context.enemy_strength, 1)

        # 选择合适战术
        if strength_ratio < 0.5:
            tactic = self._defensive_tactics(context)
        elif strength_ratio < 1.0:
            tactic = self._balanced_tactics(context)
        else:
            tactic = self._offensive_tactics(context)

        # 记录战术决策
        decision = {
            "strength_ratio": strength_ratio,
            "recommended_tactic": tactic,
            "intelligence_advice": intelligence_advice,
            "context": context.model_dump()
        }
        self.tactics_log.append(decision)

        return decision

    def _know_enemy(self, context: TacticalContext) -> str:
        """知彼知己分析"""
        if context.has_intelligence:
            return (
                "已掌握敌军情报，可采用针对性战术。"
                "孙子曰：知彼知己，百战不殆。"
            )
        return (
            "敌军情报不足，建议先派斥候侦察。"
            "孙子曰：明君贤将，能以上智为间者，必成大功。"
        )

    def _defensive_tactics(self, context: TacticalContext) -> Dict[str, str]:
        """防御战术 - 敌强我弱"""
        tactics = []

        # 先为不可胜
        tactics.append({
            "name": TacticType.DEFENSIVE_SUPERIORITY.value,
            "advice": "先为不可胜，以待敌之可胜。选择有利地形，严密防守。",
            "priority": 1
        })

        # 致人而不致于人
        if context.terrain == "山地" or context.terrain == "河流":
            tactics.append({
                "name": TacticType.CONTROL_ENEMY.value,
                "advice": "利用地形优势，使敌无法近身。",
                "priority": 2
            })
        else:
            tactics.append({
                "name": TacticType.CONTROL_ENEMY.value,
                "advice": "设置陷阱，诱敌深入后再反击。",
                "priority": 2
            })

        # 夺气
        if context.morale > 60:
            tactics.append({
                "name": TacticType.MORALE_WINNING.value,
                "advice": "保持高昂士气，等待敌军疲惫再出击。",
                "priority": 3
            })

        return {
            "strategy": "防守反击",
            "tactics": tactics,
            "principle": "善战者，立于不败之地，而不失敌之败也。"
        }

    def _balanced_tactics(self, context: TacticalContext) -> Dict[str, str]:
        """均衡战术 - 势均力敌"""
        tactics = []

        # 奇正相生
        tactics.append({
            "name": TacticType.REGULAR_VS_SPECIAL.value,
            "advice": "以正兵迎敌，以奇兵制胜。正面牵制，侧翼突击。",
            "priority": 1
        })

        # 出其不意
        if context.time_factor == "夜间":
            tactics.append({
                "name": TacticType.SURPRISE_ATTACK.value,
                "advice": "夜袭！出其不意，攻其不备。",
                "priority": 2
            })
        elif context.weather == "雨天":
            tactics.append({
                "name": TacticType.SURPRISE_ATTACK.value,
                "advice": "趁恶劣天气敌军懈怠，发动突袭。",
                "priority": 2
            })

        # 因粮于敌
        if context.supplies < 50:
            tactics.append({
                "name": TacticType.RAPID_WARFARE.value,
                "advice": "补给不足，应速战速决。'兵贵胜，不贵久'。",
                "priority": 3
            })

        return {
            "strategy": "以奇制胜",
            "tactics": tactics,
            "principle": "凡战者，以正合，以奇胜。故善出奇者，无穷如天地，不竭如江河。"
        }

    def _offensive_tactics(self, context: TacticalContext) -> Dict[str, str]:
        """进攻战术 - 我强敌弱"""
        tactics = []

        # 速战速决
        tactics.append({
            "name": TacticType.RAPID_WARFARE.value,
            "advice": "乘胜追击，不给敌军喘息之机。",
            "priority": 1
        })

        # 全军突击
        tactics.append({
            "name": TacticType.TOTAL_VICTORY.value,
            "advice": "集中优势兵力，力求全歼敌军。",
            "priority": 2
        })

        # 伐谋伐交
        if context.enemy_strength < context.self_strength * 0.3:
            tactics.append({
                "name": TacticType.STRATEGIC_ALLIANCE.value,
                "advice": "敌军士气低落，可尝试劝降，不战而屈人之兵。",
                "priority": 3
            })

        return {
            "strategy": "全面进攻",
            "tactics": tactics,
            "principle": "上兵伐谋，其次伐交，其次伐兵，其下攻城。"
        }

    def get_specific_tactic(self, tactic_type: TacticType, context: TacticalContext) -> str:
        """
        获取特定战术的详细建议

        Args:
            tactic_type: 战术类型
            context: 战术上下文

        Returns:
            战术建议文本
        """
        tactic_map = {
            TacticType.RECONNAISSANCE: "知彼知己，百战不殆。",
            TacticType.RAPID_WARFARE: "兵贵胜，不贵久。久则顿兵挫锐。",
            TacticType.TOTAL_VICTORY: "不战而屈人之兵，善之善者也。",
            TacticType.DEFENSIVE_SUPERIORITY: "先为不可胜，以待敌之可胜。",
            TacticType.REGULAR_VS_SPECIAL: "战势不过奇正，奇正相生，不可胜穷也。",
            TacticType.SURPRISE_ATTACK: "攻其无备，出其不意。",
            TacticType.CONTROL_ENEMY: "善战者，致人而不致于人。",
            TacticType.INDIRECT_APPROACH: "军争之难者，以迂为直，以患为利。",
            TacticType.ADAPTABILITY: "合于利而动，不合于利而止。",
            TacticType.ESPIONAGE: "用间者，必成大功于天下。",
        }
        return tactic_map.get(tactic_type, "战术待定...")

    def get_wisdom_quote(self) -> str:
        """获取孙子兵法名言"""
        import random
        quotes = [
            "兵者，国之大事，死生之地，存亡之道，不可不察也。",
            "知彼知己，百战不殆；不知彼而知己，一胜一负；不知彼，不知己，每战必殆。",
            "上兵伐谋，其次伐交，其次伐兵，其下攻城。",
            "善战者，立于不败之地，而不失敌之败也。",
            "兵贵胜，不贵久。",
            "知彼知己，百战不殆。",
            "其疾如风，其徐如林，侵掠如火，不动如山。",
            "知己知彼，百战不殆。",
            "上下一心，三军同力。",
            "令素行以教其民，则民服。"
        ]
        return random.choice(quotes)

    def get_tactics_log(self) -> List[Dict[str, Any]]:
        """获取战术决策日志"""
        return self.tactics_log


# ==================== 战术Agent ====================

class SunTzuAgent:
    """
    孙子兵法Agent - 提供智能战术建议

    可以与BingFu框架中的其他Agent配合使用。
    """

    def __init__(self, name: str = "孙子"):
        self.name = name
        self.engine = TacticsEngine()
        self.role = "军师"

    def analyze_battlefield(self, context: TacticalContext) -> Dict[str, Any]:
        """
        分析战场态势

        Args:
            context: 战术上下文

        Returns:
            战术分析结果
        """
        return self.engine.analyze(context)

    def recommend_tactic(self, tactic_type: TacticType, context: TacticalContext) -> str:
        """
        推荐特定战术

        Args:
            tactic_type: 战术类型
            context: 战术上下文

        Returns:
            战术建议
        """
        return self.engine.get_specific_tactic(tactic_type, context)

    def get_wisdom(self) -> str:
        """获取兵法智慧"""
        return self.engine.get_wisdom_quote()

    def __str__(self) -> str:
        return f"SunTzuAgent(name='{self.name}', role='{self.role}')"

    def __repr__(self) -> str:
        return self.__str__()


# ==================== 演示 ====================

def demo_tactics_engine():
    """孙子兵法战术引擎演示"""
    print("=" * 60)
    print("孙子兵法战术引擎演示")
    print("=" * 60)

    engine = TacticsEngine()

    # 场景1：敌强我弱
    print("\n【场景1】敌强我弱")
    print("-" * 40)
    context1 = TacticalContext(
        self_strength=30000,
        enemy_strength=80000,
        terrain="山地",
        morale=70,
        has_intelligence=False
    )
    result1 = engine.analyze(context1)
    print(f"战术分析: {result1['recommended_tactic']['strategy']}")
    for t in result1['recommended_tactic']['tactics']:
        print(f"  - {t['name']}: {t['advice']}")
    print(f"兵法要义: {result1['recommended_tactic']['principle']}")

    # 场景2：势均力敌
    print("\n【场景2】势均力敌")
    print("-" * 40)
    context2 = TacticalContext(
        self_strength=50000,
        enemy_strength=55000,
        terrain="平原",
        weather="阴天",
        morale=60,
        supplies=40,
        time_factor="黄昏",
        has_intelligence=True
    )
    result2 = engine.analyze(context2)
    print(f"战术分析: {result2['recommended_tactic']['strategy']}")
    for t in result2['recommended_tactic']['tactics']:
        print(f"  - {t['name']}: {t['advice']}")
    print(f"兵法要义: {result2['recommended_tactic']['principle']}")

    # 场景3：我强敌弱
    print("\n【场景3】我强敌弱")
    print("-" * 40)
    context3 = TacticalContext(
        self_strength=100000,
        enemy_strength=20000,
        terrain="平原",
        morale=90,
        supplies=80,
        has_intelligence=True
    )
    result3 = engine.analyze(context3)
    print(f"战术分析: {result3['recommended_tactic']['strategy']}")
    for t in result3['recommended_tactic']['tactics']:
        print(f"  - {t['name']}: {t['advice']}")
    print(f"兵法要义: {result3['recommended_tactic']['principle']}")


def demo_sun_tzu_agent():
    """孙子Agent演示"""
    print("\n" + "=" * 60)
    print("孙子兵法Agent演示")
    print("=" * 60)

    sun_tzu = SunTzuAgent()

    print(f"\n{sun_tzu.name} ({sun_tzu.role}) 上线！")

    # 获取名言
    print(f"\n{sun_tzu.get_wisdom()}")

    # 分析战场
    context = TacticalContext(
        self_strength=40000,
        enemy_strength=60000,
        terrain="河流",
        weather="雨天",
        morale=55,
        has_intelligence=True
    )

    print("\n战场态势分析：")
    result = sun_tzu.analyze_battlefield(context)
    print(f"  敌我力量比: {result['strength_ratio']:.2f}")
    print(f"  推荐策略: {result['recommended_tactic']['strategy']}")
    print(f"  情报建议: {result['intelligence_advice']}")

    # 获取特定战术
    print("\n特定战术查询 - 火攻:")
    tactic = sun_tzu.recommend_tactic(TacticType.FIRE_ATTACK, context)
    print(f"  {tactic}")


def demo_battle_simulation():
    """战役模拟"""
    print("\n" + "=" * 60)
    print("【巨鹿之战模拟 - 孙子兵法视角】")
    print("=" * 60)

    sun_tzu = SunTzuAgent()

    # 初始态势
    print("\n📜 初始态势:")
    print("  项羽率楚军五万，援赵抗秦")
    print("  秦将章邯率军四十万，围攻赵国")

    context = TacticalContext(
        self_strength=50000,
        enemy_strength=400000,
        terrain="巨鹿",
        weather="严冬",
        morale=80,  # 楚军士气高昂
        supplies=30,  # 补给线被切断
        has_intelligence=True
    )

    print("\n🧠 孙子分析:")
    result = sun_tzu.analyze_battlefield(context)
    print(f"  敌我力量比: {result['strength_ratio']:.2f} (极度劣势)")
    print(f"  推荐策略: {result['recommended_tactic']['strategy']}")

    print("\n💡 战术建议:")
    for t in result['recommended_tactic']['tactics']:
        print(f"  {t['advice']}")

    print(f"\n📜 孙子曰: {result['recommended_tactic']['principle']}")

    # 战役结果
    print("\n📜 战役结果:")
    print("  项羽破釜沉舟，率楚军九战九捷")
    print("  大破秦军，坑杀降卒二十万")
    print("  诸侯将领入帐，皆膝行而前，莫敢仰视")
    print("  项羽由此成为诸侯上将军")


if __name__ == "__main__":
    demo_tactics_engine()
    demo_sun_tzu_agent()
    demo_battle_simulation()

    print("\n" + "=" * 60)
    print("✨ 孙子兵法战术引擎演示完成！")
    print("兵法云：知彼知己，百战不殆！")
    print("=" * 60)
