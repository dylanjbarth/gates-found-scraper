results_per_page = 100 # changed from site default (12) to 100

PAYLOAD = {
		"freeTextQuery":"",
		"fieldQueries":"(@gfomediatype==\"Grant\")",
		"facetsToRender": [
			"gfocategories",
			"gfotopics",
			"gfoyear",
			"gforegions"
		],
		"page":"1", 
		"resultsPerPage": results_per_page, 
		"sortBy":"gfodate",
		"sortDirection":"desc"
	}

HEADERS = {"content-type": "application/json"}	

URL = "http://www.gatesfoundation.org/services/gfo/search.ashx"

# CATEGORIES = [
#         "Global Policy & Advocacy", 
#         "Global Health", 
#         "Global Development", 
#         "Communications", 
#         "US Program", 
#         "Special Projects"
#     ]

# REGIONS = [
#         "Europe", 
#         "Middle East, North Africa, and Greater Arabia", 
#         "Australia and Oceania", 
#         "Central America and the Caribbean", 
#         "Asia", 
#         "North America", 
#         "South America", 
#         "Sub-Saharan Africa"
#     ]

# TOPICS = [
#         "Family Health: Maternal, Newborn, and Child Health", 
#         "Scholarships", 
#         "Polio", 
#         "Africa", 
#         "Strategic Partnerships", 
#         "Vaccine Delivery", 
#         "Discovery and Translational Sciences", 
#         "Nutrition", 
#         "Integrated Development", 
#         "Not Available", 
#         "Malaria", 
#         "Global Policy & Advocacy", 
#         "Table Sponsorships", 
#         "Global Libraries", 
#         "College-Ready", 
#         "Enteric Diseases and Diarrhea", 
#         "Tuberculosis", 
#         "Community Grants", 
#         "Family Health: Nutrition", 
#         "Charitable Sector Support", 
#         "Europe", 
#         "Pacific Northwest: Early Learning", 
#         "Tobacco", 
#         "Vaccine Development", 
#         "Research & Development", 
#         "Communications", 
#         "Family Interest Grants", 
#         "Postsecondary Success", 
#         "Agricultural Development", 
#         "HIV", 
#         "Financial Services for the Poor", 
#         "Pneumonia", 
#         "Special Initiatives (Active projects are now part of other strategies)", 
#         "Water, Sanitation, and Hygiene", 
#         "India", 
#         "Emergency Response", 
#         "Community Relations", 
#         "Special Initiatives", 
#         "China", 
#         "Pacific Northwest: Family Homelessness", 
#         "Integrated Delivery", 
#         "Family Health: Family Planning", 
#         "Neglected and Infectious Diseases"
#     ]

# YEARS = [
#         "2009 and earlier", 
#         "2014", 
#         "2011", 
#         "2010", 
#         "2013", 
#         "2012"
#     ]


# def convert(first_string, lst):
# 	template_query = "(@%s==\"%s\")"
# 	setlst = set()
# 	for l in lst: 
# 		setlst.add(template_query % (first_string, l))

# 	return list(setlst)