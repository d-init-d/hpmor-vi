#!/usr/bin/env python3
"""
Fix residual fused-word issues found by extended regex scan (2026-06-02).

These 25+ fused-word corruptions were missed by the original mechanical_fix.py
because the broad fused regex only covered 5 connectors (và/thì/không/bạn/thực/
Những/anh/ấy/có). This script handles the broader set discovered in an
independent scan: một/là/rất/như/với/... and edge cases like "và o" → "vào".

Idempotent: re-running produces no changes once corpus is clean.
"""
from __future__ import annotations
import os
import sys

CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), "..", "text", "chapters")

# (chapter_filename, old_substring, new_substring) — applied in order
# Each old_substring is unique within the file to avoid double-replace.
FIXES: list[tuple[str, str, str]] = [
    # ch009:142 — Draco speech
    ("ch009-vn.txt",
     "cha biếtviệc tôi đang làm, nhưng ông ấy là người đã dạy tôi cáchlàm",
     "cha biết việc tôi đang làm, nhưng ông ấy là người đã dạy tôi cách làm"),
    ("ch009-vn.txt",
     "thì điều đó sẽ trở thành chuyện cha con và sau đó ông ấy phảimua cho tôi",
     "thì điều đó sẽ trở thành chuyện cha con và sau đó ông ấy phải mua cho tôi"),

    # ch017:33 — McGonagall speech
    ("ch017-vn.txt",
     "bị thương vĩnh viễn và tôi sẽcực kỳ khó chịunếu bạn là lớp đầu tiênlàm hỏng",
     "bị thương vĩnh viễn và tôi sẽ cực kỳ khó chịu nếu bạn là lớp đầu tiên làm hỏng"),

    # ch019:130 — Harry thinks
    ("ch019-vn.txt",
     "Anh ấy biết đại khái những gì anh ấy muốnlàm, nhưng nó phải được thực hiện theo cách mà không ai hiểu đượcnhững gìanh ấy đã làm",
     "Anh ấy biết đại khái những gì anh ấy muốn làm, nhưng nó phải được thực hiện theo cách mà không ai hiểu được những gì anh ấy đã làm"),

    # ch019:184 — McGonagall reaction
    ("ch019-vn.txt", "trôngrấttức giận.", "trông rất tức giận."),

    # ch026:137 — Draco's planning
    ("ch026-vn.txt",
     "họ sẽ phải nghĩchúng ta ngang nhau. Nếu không thì chỉ cầnmộttrong số họ",
     "họ sẽ phải nghĩ chúng ta ngang nhau. Nếu không thì chỉ cần một trong số họ"),

    # ch026:144 — Harry's expertise
    ("ch026-vn.txt",
     "không có cách nàoanh có thể ngang bằng với tôi khi chỉ đạo Âm mưu. Anh mới chỉ là nhà khoa học đượcmột ngày, anh biếtmộtbí mật về axit deoxyribonucleic, và anh chưa được đào tạo vềbất kỳphương pháp hợp lý nào",
     "không có cách nào anh có thể ngang bằng với tôi khi chỉ đạo Âm mưu. Anh mới chỉ là nhà khoa học được một ngày, anh biết một bí mật về axit deoxyribonucleic, và anh chưa được đào tạo về bất kỳ phương pháp hợp lý nào"),

    # ch026:152 — Draco's realization
    ("ch026-vn.txt",
     "thực ra điều đólàvì lợi ích của chính Harry.",
     "thực ra điều đó là vì lợi ích của chính Harry."),

    # ch035:56 — Zabini appraisal
    ("ch035-vn.txt",
     "sẽ vui lòng bán cô ấy cho bất kỳ aikhácnhưng anh ấy sẽ không bao giờ",
     "sẽ vui lòng bán cô ấy cho bất kỳ ai khác nhưng anh ấy sẽ không bao giờ"),

    # ch035:217 — Susan Bones
    ("ch035-vn.txt",
     "Chúng ta không cần phải cảnh giác nhưhọlàm!",
     "Chúng ta không cần phải cảnh giác như họ làm!"),

    # ch035:340 — Zabini's logic
    ("ch035-vn.txt",
     "chỉ vì chúng tôi đã lừahọlàm việc đó",
     "chỉ vì chúng tôi đã lừa họ làm việc đó"),

    # ch049:125 — Draco's rant about Slytherin
    ("ch049-vn.txt",
     "quanh quẩn với loại ngườilàm! Đó là tất cả những gì mọi người nghĩ Slytherinbây giờ là",
     "quanh quẩn với loại người làm! Đó là tất cả những gì mọi người nghĩ Slytherin bây giờ là"),
    ("ch049-vn.txt",
     "Những học sinhgiỏi nhấtcó đức tính ở nhiều Nhà",
     "Những học sinh giỏi nhất có đức tính ở nhiều Nhà"),
    ("ch049-vn.txt",
     "của Slytherin với bất kỳ aikhông bị mọi sự thù hận đẩy lùi.",
     "của Slytherin với bất kỳ ai không bị mọi sự thù hận đẩy lùi."),

    # ch049:208 — Harry explaining
    ("ch049-vn.txt",
     "một phầncủa cậu, ” Harry nói.",
     "một phần của cậu, ” Harry nói."),
    ("ch049-vn.txt",
     "Cố gắng để cậulàm tốt hơn.",
     "Cố gắng để cậu làm tốt hơn."),
    ("ch049-vn.txt",
     "việc sửa chữa Nhà Slytherin cũng có thể cầncái đó",
     "việc sửa chữa Nhà Slytherin cũng có thể cần cái đó"),

    # ch049:274 — Harry's conditions
    ("ch049-vn.txt",
     "tôi biếtlàcậunói rằngLuciusnói rằngcụ Dumbledorenói rằng ông đã giết Narcissa.",
     "tôi biết là cậu nói rằng Lucius nói rằng cụ Dumbledore nói rằng ông đã giết Narcissa."),
    ("ch049-vn.txt",
     "Điều kiện đầu tiên là tại bất kỳ thời điểm nàobạn có thể giải phóng",
     "Điều kiện đầu tiên là tại bất kỳ thời điểm nào bạn có thể giải phóng"),

    # ch061:96 — Hermione's thought
    ("ch061-vn.txt", "Điều cô ấy cầnlàm là tìm ra", "Điều cô ấy cần làm là tìm ra"),

    # ch079:182 — Hermione under cloak
    ("ch079-vn.txt",
     "Việc trở nên vô hình lẽ ra phảithú vị hơn thế này",
     "Việc trở nên vô hình lẽ ra phải thú vị hơn thế này"),
    ("ch079-vn.txt",
     "cô ấy không chắc mìnhmuốnlàm vậy.",
     "cô ấy không chắc mình muốn làm vậy."),
    ("ch079-vn.txt",
     "Đó là một cảm giác đáng lo ngại, không hẳn làvô hìnhmà là không tồn tại.",
     "Đó là một cảm giác đáng lo ngại, không hẳn là vô hình mà là không tồn tại."),

    # ch079:235 — Dementor/Bartemius voice
    ("ch079-vn.txt",
     "“Bạnlàngười thông minh, ” giọng nói nói",
     "“Bạn là người thông minh, ” giọng nói nói"),

    # ch088:60 — Harry explaining prophecy
    ("ch088-vn.txt",
     "hơi lố khi chỉ mô tảnhững sự kiện lịch sử đã xảy ra",
     "hơi lố khi chỉ mô tả những sự kiện lịch sử đã xảy ra"),
    ("ch088-vn.txt",
     "coi lời tiên tri là vềmột sốtương lai có thể xảy ra",
     "coi lời tiên tri là về một số tương lai có thể xảy ra"),
    ("ch088-vn.txt",
     "chỉmộttrong số đó thực sự được hiện thực hóa",
     "chỉ một trong số đó thực sự được hiện thực hóa"),

    # ch088:108 — Harry: a Death Eater?
    ("ch088-vn.txt",
     "“Đợi đã, chờ đã—bạn là mộtTử thần Thực tử?”",
     "“Đợi đã, chờ đã—bạn là một Tử thần Thực tử?”"),

    # ch088:138 — Harry internal voice
    ("ch088-vn.txt",
     "chúng ta đã không hề thay đổi niềm tinsau khi gặp phải",
     "chúng ta đã không hề thay đổi niềm tin sau khi gặp phải"),
    ("ch088-vn.txt",
     "mối đe dọa nghiêm trọnglàban đầu dựa trên việc Dấu hiệu Hắc ám ngu ngốc",
     "mối đe dọa nghiêm trọng là ban đầu dựa trên việc Dấu hiệu Hắc ám ngu ngốc"),

    # ch088:445 — Harry observes Slytherin
    ("ch088-vn.txt",
     "Tuy nhiên, điều đólàhiển nhiên, đã quan sát phần Slytherin của mình.",
     "Tuy nhiên, điều đó là hiển nhiên, đã quan sát phần Slytherin của mình."),

    # ch088:526 — McGonagall gives Harry a look
    ("ch088-vn.txt",
     "Giáo sư McGonagall ném cho Harry một cái nhìnrấtkỳ lạ.",
     "Giáo sư McGonagall ném cho Harry một cái nhìn rất kỳ lạ."),

    # ch099:129 — Draco's plan
    ("ch099-vn.txt",
     "nếu họ nghĩ rằng Cha thậm chí đã cố gắnglàm điều gì đó như vậy",
     "nếu họ nghĩ rằng Cha thậm chí đã cố gắng làm điều gì đó như vậy"),

    # ch099:152 — Harry ponders
    ("ch099-vn.txt",
     "“Nếulàcụ Dumbledore, thì việc loại ông ấy khỏi bàn cờ",
     "“Nếu là cụ Dumbledore, thì việc loại ông ấy khỏi bàn cờ"),

    # ch111:138 — Quirrell's monologue (vào mis-typed as "và o")
    ("ch111-vn.txt",
     "hãy nhìn và ohậu quả và hỏi xem liệu chúng có chủ ý hay không.",
     "hãy nhìn vào hậu quả và hỏi xem liệu chúng có chủ ý hay không."),
    ("ch111-vn.txt",
     "các Slytherin xếp và ohàng ngũ thuộc hạ của ta",
     "các Slytherin xếp vào hàng ngũ thuộc hạ của ta"),
    ("ch111-vn.txt",
     "cụ Dumbledore đưa và olàm Người đứng đầu Slytherin là Severus Snape",
     "cụ Dumbledore đưa vào làm Người đứng đầu Slytherin là Severus Snape"),
    ("ch111-vn.txt",
     "Giáo sư Quirrell thả và ovạc một cục nước đá",
     "Giáo sư Quirrell thả vào vạc một cục nước đá"),
    ("ch111-vn.txt",
     "khi nó chạm và obề mặt sủi bọt.",
     "khi nó chạm vào bề mặt sủi bọt."),
    ("ch111-vn.txt",
     "sẽ không có đứa trẻ nào muốn và oSlytherin.",
     "sẽ không có đứa trẻ nào muốn vào Slytherin."),
    ("ch111-vn.txt",
     "sẽ được phân bổ và oba Nhà còn lại.",
     "sẽ được phân bổ vào ba Nhà còn lại."),
    ("ch111-vn.txt",
     "không có Nhà Trẻ hư nào được thêm và ohỗn hợp;",
     "không có Nhà Trẻ hư nào được thêm vào hỗn hợp;"),
    ("ch111-vn.txt",
     "đã đủ khôn ngoan để từ chối Salazar Slytherin và ohọc của họ.",
     "đã đủ khôn ngoan để từ chối Salazar Slytherin vào học của họ."),

    # ch111:207 — Harry's tearful moment
    ("ch111-vn.txt",
     "một người ban cho bạn sự bất tửnghĩa là, một người mà bạn muốn sống mãi mãivớibạn",
     "một người ban cho bạn sự bất tử nghĩa là, một người mà bạn muốn sống mãi mãi với bạn"),
]


def main() -> int:
    if not FIXES:
        print("No fixes registered.")
        return 0

    # Group fixes by file
    by_file: dict[str, list[tuple[str, str]]] = {}
    for fn, old, new in FIXES:
        by_file.setdefault(fn, []).append((old, new))

    total_changes = 0
    total_already = 0
    for fn, edits in sorted(by_file.items()):
        path = os.path.join(CHAPTERS_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        file_changes = 0
        for old, new in edits:
            count = text.count(old)
            if count == 0:
                # Check if the new form is already present
                if new in text:
                    total_already += 1
                else:
                    print(f"  [WARN] {fn}: old not found: {old[:60]}…")
                continue
            if count > 1:
                print(f"  [WARN] {fn}: old appears {count}×: {old[:60]}…")
            text = text.replace(old, new, 1)
            file_changes += count
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        if file_changes:
            print(f"  ✅ {fn}: {file_changes} fix(es)")
        total_changes += file_changes

    print()
    print(f"Total fixes applied: {total_changes}")
    if total_already:
        print(f"  ({total_already} old form(s) absent — likely already fixed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
