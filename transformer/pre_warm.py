from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

ARTICLE = """
Fisheries and Oceans Canada conducted an ecosystem-based survey from October 6-16,
2020 on the CCGS Sir John Franklin. This study targeted juvenile Pacific Salmon from Queen
Charlotte Sound to Dixon Entrance.
There were 26 species sampled in 1741 kg of catch, with 25% Pacific Salmon caught by weight.
Overall, Opalescent Inshore Squid (45%) and Moon Jellyfish (26%) were the most abundant
species by weight. Lengths and weights were recorded for 17 species, including all 5 Pacific
Salmon species (Oncorhynchus spp.). Juvenile Chum Salmon were the most abundant Pacific
Salmon species with large catches, particularly in Hecate Strait, and only 2% containing empty
stomachs. Pink Salmon were the most widespread species, whereas juvenile Sockeye Salmon
were localized in northern Dixon Entrance. Both juvenile Pink Salmon and Sockeye Salmon were
primarily feeding on euphausiids and amphipods. Juvenile Coho Salmon were less abundant
and were caught in Dixon Entrance and Hecate Strait, to a lesser amount. Juvenile Coho Salmon
had 47% empty stomachs and the widest variety of prey in their stomach contents. Only three
Chinook Salmon were caught. The only Chinook Salmon with stomach contents contained
Squid.
Biological samples for genetic stock composition and energy density are at the Pacific Biological
Station, Fisheries and Oceans Canada (Nanaimo, BC) for laboratory analysis. Associated
information on the physical oceanography and zooplankton composition was collected from
21 stations, and will be analysed at the the Institute of Ocean Sciences, Fisheries and Oceans
Canada (Sidney, BC).
In addition, gear optimization occurred for the 2022 Pan-Pacific High Seas Expedition. The
protocols for the offshore LFS 1142 trawl net, MOCNESS (Multiple Opening and Closing Net
with Environmental Sensing System), oblique zooplankton tows, and CTD rosette deployment
using the Launch and Recovery System (LARS) were tested.
"""

summarizer = pipeline("summarization")
print(summarizer(ARTICLE, max_length=4096, min_length=30, do_sample=False))
