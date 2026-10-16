import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 800, "Évaluation Sommative MicroPython - Terminale SI | Bilan & Fiches Individuelles")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        # Footer
        page_text = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(541, 35, page_text)
        self.drawString(54, 35, "Lycée - Sciences de l'Ingénieur | Spécialité SI")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 541, 48)
        self.restoreState()

def create_evaluation_pdf(filename="Correction_Copies_MicroPython_Terminale_SI.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1e293b'),
        alignment=1, # Center
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    comment_style = ParagraphStyle(
        'Comment',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f172a')
    )

    note_badge_style = ParagraphStyle(
        'NoteBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=2,
        textColor=colors.HexColor('#1e40af')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.white
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#1e293b')
    )

    table_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    table_cell_left_bold = ParagraphStyle(
        'TableCellLeftBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # ================= PAGE 1 : RÉCAPITULATIF GLOBAL =================
    story.append(Paragraph("BULLETIN D'ÉVALUATION SOMMATIVE", title_style))
    story.append(Paragraph("<b>Discipline :</b> Sciences de l'Ingénieur &bull; <b>Niveau :</b> Terminale SI &bull; <b>Classe :</b> TG1<br/><b>Objet :</b> MicroPython sur Raspberry Pi Pico (GPIO TOR, PWM, CAN & Algorithmique)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3b82f6'), spaceBefore=0, spaceAfter=12))

    story.append(Paragraph("1. Tableau Récapitulatif des Résultats", h1_style))

    # Data for summary table
    summary_data = [
        [
            Paragraph("Rang", table_header_style),
            Paragraph("Élève", table_header_style),
            Paragraph("Ex 1 (/4)<br/><font size=6.5>Bouton & Temporisation</font>", table_header_style),
            Paragraph("Ex 2 (/4)<br/><font size=6.5>CAN & PWM Buzzer</font>", table_header_style),
            Paragraph("Ex 3 (/6)<br/><font size=6.5>Feu Tricolore</font>", table_header_style),
            Paragraph("Ex 4 (/6)<br/><font size=6.5>Alerte Multi-seuils</font>", table_header_style),
            Paragraph("Total (/20)", table_header_style),
            Paragraph("Appréciation synthétique", table_header_style)
        ],
        [
            Paragraph("1<sup>er</sup>", table_cell_center),
            Paragraph("<b>JOLLY Louison</b>", table_cell_left_bold),
            Paragraph("3,50", table_cell_center),
            Paragraph("4,00", table_cell_center),
            Paragraph("6,00", table_cell_center),
            Paragraph("5,50", table_cell_center),
            Paragraph("<b>19,00</b>", table_cell_center),
            Paragraph("Excellent travail, rigueur logique et maîtrise du principe DRY.", table_cell_left)
        ],
        [
            Paragraph("2<sup>e</sup>", table_cell_center),
            Paragraph("<b>MOLLA Victor</b>", table_cell_left_bold),
            Paragraph("3,00", table_cell_center),
            Paragraph("4,00", table_cell_center),
            Paragraph("5,75", table_cell_center),
            Paragraph("6,00", table_cell_center),
            Paragraph("<b>18,75</b>", table_cell_center),
            Paragraph("Remarquable, compréhension parfaite du PWM et du CAN.", table_cell_left)
        ],
        [
            Paragraph("3<sup>e</sup>", table_cell_center),
            Paragraph("<b>LETOT Nathan</b>", table_cell_left_bold),
            Paragraph("2,75", table_cell_center),
            Paragraph("4,00", table_cell_center),
            Paragraph("6,00", table_cell_center),
            Paragraph("5,75", table_cell_center),
            Paragraph("<b>18,50</b>", table_cell_center),
            Paragraph("Très solide, explications PWM limpides et code soigné.", table_cell_left)
        ],
        [
            Paragraph("4<sup>e</sup>", table_cell_center),
            Paragraph("<b>PAIVA Elio</b>", table_cell_left_bold),
            Paragraph("3,50", table_cell_center),
            Paragraph("2,75", table_cell_center),
            Paragraph("6,00", table_cell_center),
            Paragraph("6,00", table_cell_center),
            Paragraph("<b>18,25</b>", table_cell_center),
            Paragraph("Très haute maîtrise algorithmique, fiches de code parfaites.", table_cell_left)
        ],
        [
            Paragraph("5<sup>e</sup>", table_cell_center),
            Paragraph("<b>MUZEREAU Maïllie</b>", table_cell_left_bold),
            Paragraph("3,50", table_cell_center),
            Paragraph("2,50", table_cell_center),
            Paragraph("6,00", table_cell_center),
            Paragraph("5,50", table_cell_center),
            Paragraph("<b>17,50</b>", table_cell_center),
            Paragraph("Très bon devoir, logique très claire. Attention au PWM ex 2.", table_cell_left)
        ],
        [
            Paragraph("6<sup>e</sup>", table_cell_center),
            Paragraph("<b>MONCELET Jules</b>", table_cell_left_bold),
            Paragraph("2,00", table_cell_center),
            Paragraph("2,75", table_cell_center),
            Paragraph("4,50", table_cell_center),
            Paragraph("5,00", table_cell_center),
            Paragraph("<b>14,25</b>", table_cell_center),
            Paragraph("Bon travail. Revoir le passage des arguments dans une fonction.", table_cell_left)
        ],
        [
            Paragraph("7<sup>e</sup>", table_cell_center),
            Paragraph("<b>RENAUD-LOMBARD Mathou</b>", table_cell_left_bold),
            Paragraph("2,25", table_cell_center),
            Paragraph("3,00", table_cell_center),
            Paragraph("2,50", table_cell_center),
            Paragraph("5,00", table_cell_center),
            Paragraph("<b>12,75</b>", table_cell_center),
            Paragraph("Ensemble convenable. Confusions sur la fonction du feu tricolore.", table_cell_left)
        ],
        [
            Paragraph("8<sup>e</sup>", table_cell_center),
            Paragraph("<b>BELLIN Jean</b>", table_cell_left_bold),
            Paragraph("1,75", table_cell_center),
            Paragraph("2,00", table_cell_center),
            Paragraph("3,50", table_cell_center),
            Paragraph("5,00", table_cell_center),
            Paragraph("<b>12,25</b>", table_cell_center),
            Paragraph("Moyenne atteinte mais des bases à consolider (formules, fonctions).", table_cell_left)
        ]
    ]

    t_summary = Table(
        summary_data,
        colWidths=[32, 90, 48, 52, 48, 52, 48, 117]
    )
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 14))

    # Stat box
    stat_data = [
        [
            Paragraph("<b>Moyenne de classe :</b> 15,16 / 20", body_style),
            Paragraph("<b>Note Max :</b> 19,00 / 20", body_style),
            Paragraph("<b>Note Min :</b> 12,25 / 20", body_style),
            Paragraph("<b>Taux de réussite :</b> 100 % (&ge; 10/20)", body_style)
        ]
    ]
    t_stat = Table(stat_data, colWidths=[120, 100, 100, 167])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bfdbfe')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_stat)
    story.append(Spacer(1, 14))

    story.append(Paragraph("2. Synthèse Pédagogique par Exercice", h1_style))
    
    synth_text = """
    <b>&bull; Exercice 1 (TOR & temporisation - 4 pts) :</b> La gestion temporelle du clignotement et l'analyse de la condition logique inversée (<code>not etat_bouton</code>) sont globalement bien comprises. La durée totale de 1,2 s est calculée avec succès par la quasi-totalité des élèves. En revanche, le rôle matériel du Pull-Up (éviter l'état flottant / haute impédance) reste mal verbalisé et le principe <b>DRY</b> n'a été expressément nommé que par Louison Jolly.<br/>
    <b>&bull; Exercice 2 (CAN & PWM Buzzer - 4 pts) :</b> Le calcul du quantum et de la tension (2,20 V) est maîtrisé par 100% des élèves, tout comme la relation T = 1/f (2 ms). La principale difficulté réside dans la représentation graphique du PWM (plusieurs élèves ont tracé une tension continue constante au lieu d'un créneau 0V / 3,3V à rapport cyclique 50%) et la lecture du code pour remplir le tableau fonctionnel.<br/>
    <b>&bull; Exercice 3 (Feu tricolore carrefour - 6 pts) :</b> Excellente réussite sur les temporisations et l'algorithme global. Néanmoins, 3 élèves ont écrit des valeurs fixes en dur (<code>value(1)</code>) à l'intérieur du corps de la fonction <code>activer_feu</code> au lieu de réutiliser les arguments passés en paramètre.<br/>
    <b>&bull; Exercice 4 (Centrale d'alerte progressive - 6 pts) :</b> Très bonne maîtrise de la configuration PWM et de la logique à multi-seuils. L'erreur la plus fréquente porte sur la méthode de lecture de l'ADC : confusion entre <code>read_u16()</code>, <code>duty_u16()</code> et <code>value()</code>.
    """
    story.append(Paragraph(synth_text, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Compétences du Programme SI Évaluées", h1_style))
    
    comp_data = [
        [
            Paragraph("<b>Réf.</b>", table_cell_center),
            Paragraph("<b>Compétence évaluée</b>", table_cell_left_bold),
            Paragraph("<b>Niveau de maîtrise constaté</b>", table_cell_left_bold)
        ],
        [
            Paragraph("CO3.1", table_cell_center),
            Paragraph("Identifier les grandeurs physiques et logiques (Tension, Période, Fréquence, Pull-Up/Pull-Down)", table_cell_left),
            Paragraph("<font color='#16a34a'><b>Très satisfaisant</b></font> (Calculs CAN et f/T parfaitement maîtrisés)", table_cell_left)
        ],
        [
            Paragraph("CO3.2", table_cell_center),
            Paragraph("Associer une modulation PWM à une commande de puissance ou un avertisseur sonore", table_cell_left),
            Paragraph("<font color='#ca8a04'><b>Satisfaisant</b></font> (Principe compris, chronogramme créneau à consolider)", table_cell_left)
        ],
        [
            Paragraph("CO5.1", table_cell_center),
            Paragraph("Concevoir et programmer un algorithme séquentiel et conditionnel (MicroPython)", table_cell_left),
            Paragraph("<font color='#16a34a'><b>Très satisfaisant</b></font> (Structures if/elif/else et boucles bien gérées)", table_cell_left)
        ],
        [
            Paragraph("CO5.2", table_cell_center),
            Paragraph("Modularité logicielle : création et appel de fonctions avec passage de paramètres (Principe DRY)", table_cell_left),
            Paragraph("<font color='#ea580c'><b>À consolider</b></font> (Distinction argument formel vs valeur en dur à revoir)", table_cell_left)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[45, 230, 212])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Plan de Remédiation Pédagogique Préconisé", h1_style))
    remed_text = """
    <b>1. Remédiation 'Fonctions et Paramètres' (30 min) :</b> Mini-activité sur le passage d'arguments (différence entre le paramètre formel dans <code>def</code> et la valeur effective passée lors de l'appel) pour lever les confusions observées chez Jean, Jules et Mathou.<br/>
    <b>2. Remédiation 'Modulation PWM à l'oscilloscope' (15 min) :</b> Visualisation en direct sur carte ou simulateur de l'effet d'une variation de <code>duty_u16</code> sur l'allure du créneau (rapport cyclique) pour corriger les représentations en tension continue plate.<br/>
    <b>3. Fiche mémo 'Méthodes MicroPython' :</b> Récapituler sur un pense-bête les méthodes clés : <code>Pin.value()</code> (TOR), <code>ADC.read_u16()</code> (CAN 16b), <code>PWM.duty_u16()</code> et <code>PWM.freq()</code> (PWM).
    """
    story.append(Paragraph(remed_text, body_style))

    story.append(PageBreak())

    # ================= FICHES ÉLÈVES (2 élèves par page ou 1 élève par page) =================
    # Let's inspect the data for each student to render clean individual cards.
    # 8 students -> let's make 2 students per page (total 4 pages) = 5 pages total!
    # That gives plenty of space for each student: a nice card with details per exercise and personal comment.

    students = [
        {
            "nom": "JOLLY Louison",
            "classe": "TG1",
            "note": "19,00 / 20",
            "rang": "1er sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "3,50 / 4", "Calculs temporels parfaits (1,2 s). Principe DRY cité textuellement. Mentionner plus clairement le rôle anti-flottant du Pull-up."),
                ("Ex 2 : CAN & PWM Buzzer", "4,00 / 4", "Copie parfaite : conversion 2,20 V, période 2 ms, chronogramme PWM créneau impeccable et tableau fonctionnel exact."),
                ("Ex 3 : Feu Carrefour", "6,00 / 6", "Code exemplaire : déclarations, fonction paramétrée et séquencement temporel irréprochables."),
                ("Ex 4 : Centrale d'alerte", "5,50 / 6", "Très bonne gestion des seuils et de la PWM. Seule étourderie : appel de .value() au lieu de .read_u16().")
            ],
            "appreciation": "Remarquable copie démontrant une excellente rigueur d'analyse et une compréhension fine du matériel et du code MicroPython. Bravo !"
        },
        {
            "nom": "MOLLA Victor",
            "classe": "TG1",
            "note": "18,75 / 20",
            "rang": "2e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "3,00 / 4", "Temporisations (1,2 s) et logique d'inversion très bien assimilées. Rôle physique du Pull-Up non rédigé."),
                ("Ex 2 : CAN & PWM Buzzer", "4,00 / 4", "Excellente maîtrise : formule CAN posée avec précision, chronogramme PWM juste et tableau complet avec pourcentages."),
                ("Ex 3 : Feu Carrefour", "5,75 / 6", "Algorithme parfait. Attention : bp_pieton.value() == TRUE provoque une erreur de syntaxe (écrire 1 ou True)."),
                ("Ex 4 : Centrale d'alerte", "6,00 / 6", "Code parfait : syntaxe .read_u16() exacte, temporisations et paramètres PWM impeccables.")
            ],
            "appreciation": "Très grand sérieux et excellente compréhension des notions de régulation et d'acquisition analogique/numérique. Travail de grande qualité."
        },
        {
            "nom": "LETOT Nathan",
            "classe": "TG1",
            "note": "18,50 / 20",
            "rang": "3e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "2,75 / 4", "Bonne gestion du clignotement. Erreur sur la valeur logique au repos du Pull-Up (vaut 1, non 0)."),
                ("Ex 2 : CAN & PWM Buzzer", "4,00 / 4", "Parfait. Remarquable explication du rapport cyclique (1 ms à 100% et 1 ms à 0%) et note musicale pertinente."),
                ("Ex 3 : Feu Carrefour", "6,00 / 6", "Code parfait : fonction paramétrée bien comprise et respect scrupuleux du cahier des charges."),
                ("Ex 4 : Centrale d'alerte", "5,75 / 6", "Très bon travail. Seule petite coquille : omission de '_u16' dans la méthode read_u16().")
            ],
            "appreciation": "Très solide prestation. Les concepts physiques et algorithmiques sont très bien assimilés. Bravo pour la précision des explications sur le PWM."
        },
        {
            "nom": "PAIVA Elio",
            "classe": "TG1",
            "note": "18,25 / 20",
            "rang": "4e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "3,50 / 4", "La meilleure explication de la classe sur l'état flottant et les parasites. Durée 1,2 s bien calculée."),
                ("Ex 2 : CAN & PWM Buzzer", "2,75 / 4", "Calculs CAN et chronogramme parfaits. Attention : unité de la fréquence = Hertz (non Henry) et confusion dans le tableau 2.4."),
                ("Ex 3 : Feu Carrefour", "6,00 / 6", "Code irréprochable et très soigné."),
                ("Ex 4 : Centrale d'alerte", "6,00 / 6", "Parfait. Seul avec Victor à avoir écrit d'emblée la méthode exacte .read_u16().")
            ],
            "appreciation": "Excellente copie témoignant d'une réflexion physique et algorithmique très mature. Veillez simplement à bien lire les consignes des tableaux fonctionnels."
        },
        {
            "nom": "MUZEREAU Maïllie",
            "classe": "TG1",
            "note": "17,50 / 20",
            "rang": "5e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "3,50 / 4", "Très bonne analyse logique de l'inversion et calcul temporel rigoureux (1,2 s)."),
                ("Ex 2 : CAN & PWM Buzzer", "2,50 / 4", "Calculs 2,20 V et T = 2 ms justes. Dessin du PWM continu (non créneau) et tableau 2.4 confondu avec le CAN."),
                ("Ex 3 : Feu Carrefour", "6,00 / 6", "Code complet, structuré et sans aucune erreur."),
                ("Ex 4 : Centrale d'alerte", "5,50 / 6", "Très bonne boucle d'alerte. Attention : l'ADC se lit avec .read_u16() et non .duty_u16() (réservé au PWM).")
            ],
            "appreciation": "Très bon ensemble, raisonnement logique clair et code très bien maîtrisé. Revoir la distinction entre la génération PWM et la lecture analogique."
        },
        {
            "nom": "MONCELET Jules",
            "classe": "TG1",
            "note": "14,25 / 20",
            "rang": "6e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "2,00 / 4", "Durée d'animation bien détaillée (1,2 s). Revoir le comportement électrique du Pull-Up (3,3 V au repos)."),
                ("Ex 2 : CAN & PWM Buzzer", "2,75 / 4", "Calcul 2,20 V et période 2 ms justes. Le PWM est un signal créneau 0-3,3V et non une tension continue moyenne."),
                ("Ex 3 : Feu Carrefour", "4,50 / 6", "Bonne gestion du cycle. Erreur : avoir mis des 1 en dur dans la fonction au lieu des variables rouge, jaune, vert."),
                ("Ex 4 : Centrale d'alerte", "5,00 / 6", "Bonne boucle d'alerte. Attention à l'opérateur 'and' et à la syntaxe exacte .read_u16().")
            ],
            "appreciation": "Résultats satisfaisants et réguliers. Il faut consolider la notion de fonction paramétrée (passage d'arguments) et la nature impulsionnelle du signal PWM."
        },
        {
            "nom": "RENAUD-LOMBARD Mathou",
            "classe": "TG1",
            "note": "12,75 / 20",
            "rang": "7e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "2,25 / 4", "Niveaux de repos trouvés. Erreur sur le calcul temporel global (1,8 s au lieu de 1,2 s)."),
                ("Ex 2 : CAN & PWM Buzzer", "3,00 / 4", "Bons calculs (2,20 V et 2 ms) et tableau bien renseigné. Chronogramme PWM à revoir en créneau."),
                ("Ex 3 : Feu Carrefour", "2,50 / 6", "Confusion majeure : écriture de 'Pull_Down' dans led.value() au lieu des variables reçues en argument ; délais inversés."),
                ("Ex 4 : Centrale d'alerte", "5,00 / 6", "Bonne gestion de la centrale d'alerte. Attention aux opérateurs logiques ('and') et aux arguments de range().")
            ],
            "appreciation": "Le niveau moyen est atteint avec de bonnes bases sur le calcul numérique et le PWM, mais des confusions conceptuelles importantes persistent sur les fonctions."
        },
        {
            "nom": "BELLIN Jean",
            "classe": "TG1",
            "note": "12,25 / 20",
            "rang": "8e sur 8",
            "details": [
                ("Ex 1 : Bouton & Temporisation", "1,75 / 4", "Niveaux électriques de repos identifiés. Explications du rôle matériel et du principe de conception incomplètes."),
                ("Ex 2 : CAN & PWM Buzzer", "2,00 / 4", "Calcul CAN juste (2,20 V). La formule de la période est T = 1/f (et non un produit avec le CAN). Signal PWM non créneau."),
                ("Ex 3 : Feu Carrefour", "3,50 / 6", "Déclarations justes. Erreur conceptuelle : valeurs fixées en dur dans la fonction au lieu des paramètres rouge, jaune, vert."),
                ("Ex 4 : Centrale d'alerte", "5,00 / 6", "Bonne structure globale. Omission de la méthode de lecture ADC et confusion entre 'or' et 'and'.")
            ],
            "appreciation": "L'évaluation est validée, mais des révisions s'imposent sur la relation période-fréquence, la structure d'une fonction et l'utilisation des connecteurs logiques."
        }
    ]

    for i, s in enumerate(students):
        # Card container
        card_content = []
        
        # Student header table
        header_table_data = [
            [
                Paragraph(f"<b>Élève :</b> {s['nom']}<br/><font color='#64748b' size=8>Classe : {s['classe']} &bull; Rang : {s['rang']}</font>", card_title_style),
                Paragraph(f"Note : {s['note']}", note_badge_style)
            ]
        ]
        t_header = Table(header_table_data, colWidths=[350, 137])
        t_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
        ]))
        card_content.append(t_header)

        # Details table
        details_table_data = [
            [
                Paragraph("<b>Exercice / Thématique</b>", table_cell_left_bold),
                Paragraph("<b>Barème</b>", table_cell_center),
                Paragraph("<b>Observations & Analyse des acquis</b>", table_cell_left_bold)
            ]
        ]
        for title, note, obs in s['details']:
            details_table_data.append([
                Paragraph(title, table_cell_left),
                Paragraph(f"<b>{note}</b>", table_cell_center),
                Paragraph(obs, table_cell_left)
            ])

        t_details = Table(details_table_data, colWidths=[130, 52, 305])
        t_details.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        card_content.append(t_details)

        # Appreciation box
        appr_data = [
            [
                Paragraph(f"<b>Appréciation globale du professeur :</b><br/>{s['appreciation']}", comment_style)
            ]
        ]
        t_appr = Table(appr_data, colWidths=[487])
        t_appr.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        card_content.append(t_appr)
        card_content.append(Spacer(1, 14))

        story.append(KeepTogether(card_content))

        # 2 students per page -> page break after even indices (index 1, 3, 5)
        if i % 2 == 1 and i < len(students) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF généré avec succès : {filename}")

if __name__ == '__main__':
    create_evaluation_pdf()
