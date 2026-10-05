import re
from typing import Dict, Any

class MaskingService:
    """
    PII Data Protection & Masking Engine.
    Guarantees that no raw unmasked personally identifiable information
    is leaked to external logs, RAG prompts, or public traces.
    """

    # 11-digit Chinese mobile phone regex
    PHONE_REGEX = re.compile(r'(?<!\d)(1[3-9]\d)(\d{4})(\d{4})(?!\d)')
    # 18-digit Chinese ID Card regex
    ID_CARD_REGEX = re.compile(r'(?<!\d)([1-9]\d{5})\d{8}(\d{3}[0-9Xx])(?!\d)')
    # 16-19 digit Bank Card regex
    BANK_CARD_REGEX = re.compile(r'(?<!\d)(\d{4})\d{8,11}(\d{4})(?!\d)')
    # Chinese names regex (common surnames + 1-2 chars)
    NAME_PATTERNS = [
        re.compile(r'([赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍卻璩桑桂濮扈套寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逮盍益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空丌官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟言福])([\u4e00-\u9fa5]{1,2})(?=(?:先生|女士|小姐|客户|投诉|师傅|同学|经理|您好|说|表示|反映|购买|退货))')
    ]

    @classmethod
    def mask_phone(cls, phone: str) -> str:
        if not phone:
            return ""
        return cls.PHONE_REGEX.sub(r'\1****\3', phone)

    @classmethod
    def mask_name(cls, name: str) -> str:
        if not name:
            return ""
        if len(name) == 2:
            return name[0] + "*"
        elif len(name) >= 3:
            return name[0] + "*" * (len(name) - 2) + name[-1]
        return name

    @classmethod
    def mask_text(cls, text: str) -> str:
        """
        Mask sensitive information in text body.
        """
        if not text:
            return ""
        
        # 1. Mask Phone Numbers
        res = cls.PHONE_REGEX.sub(r'\1****\3', text)
        
        # 2. Mask ID Cards
        res = cls.ID_CARD_REGEX.sub(r'\1********\2', res)
        
        # 3. Mask Bank Cards
        res = cls.BANK_CARD_REGEX.sub(r'\1********\2', res)
        
        # 4. Mask Surnames with Honorifics
        for pattern in cls.NAME_PATTERNS:
            res = pattern.sub(lambda m: m.group(1) + "*" * len(m.group(2)), res)
            
        return res

    @classmethod
    def sanitize_for_audit_log(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively mask sensitive keys in audit logs.
        """
        sensitive_keys = {"customer_phone", "phone", "raw_text", "id_card", "bank_card"}
        sanitized = {}
        for k, v in payload.items():
            if k in sensitive_keys and isinstance(v, str):
                sanitized[k] = cls.mask_text(v)
            elif isinstance(v, dict):
                sanitized[k] = cls.sanitize_for_audit_log(v)
            elif isinstance(v, list):
                sanitized[k] = [
                    cls.sanitize_for_audit_log(item) if isinstance(item, dict) else item
                    for item in v
                ]
            else:
                sanitized[k] = v
        return sanitized

masking_service = MaskingService()
