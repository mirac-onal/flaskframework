from flask import Flask, request, render_template
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    data = {
        "kaynakID": request.form["kaynakID"],
        "kaynakAdi": request.form["kaynakAdi"],
        "kaynakDetay": request.form["kaynakDetay"],
        "KaynakURL": request.form["KaynakURL"],
        "kaynakZamanDamgasi": request.form["kaynakZamanDamgasi"]
    }
    
    root = ET.Element("WebKaynaklari")
    kaynak = ET.SubElement(root, "Kaynak")
    
    for key, value in data.items():
        ET.SubElement(kaynak, key).text = value
    
    tree = ET.ElementTree(root)
    tree.write("data.xml", encoding="utf-8", xml_declaration=True)
    
    return "Veri başarıyla kaydedildi."


@app.route("/generate_report", methods=["POST"])
def generate_report():
    tree = ET.parse("data.xml")
    root = tree.getroot()

    report_data = []
    for kaynak in root.findall("Kaynak"):
        report_data.append({
            "kaynakID": kaynak.find("kaynakID").text,
            "KaynakURL": kaynak.find("KaynakURL").text,
            "status": kaynak.get("durum", "Bilinmiyor")
        })

    save_report_to_txt(report_data)
    return "Rapor başarıyla oluşturuldu."   