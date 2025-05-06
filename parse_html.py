from bs4 import BeautifulSoup

import requests

url = "https://materials.colabfit.org"
response = requests.get(url)
html = response.text

# Load the HTML
soup = BeautifulSoup(html, 'html.parser')

# grab cards
cards = soup.find_all('div', class_='card px-0')


combined_html = ''.join(str(card) for card in cards)

# Parse the combined HTML into a new BeautifulSoup object
combined_soup = BeautifulSoup(combined_html, 'html.parser')

# Remove buttons by class name or ID
for tag in combined_soup.select('a#download-dataset-archive'):
    tag.decompose()  # remove it from the tree

# modify hyperlink
for a in combined_soup.select('h5.card-header a'):
    href = a.get('href', '')
    if href.startswith('/id/'):
        # Prepend the base URL
        a['href'] = f"https://materials.colabfit.org{href}"

soup_txt = str(combined_soup.prettify())


top_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ColabFit Dataset Page</title>

  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Project",
      "id": "https://materials.colabfit.org",
      "logo": "https://colabfit.org/images/colabfit-logo-600.png",
      "url": "https://materials.colabfit.org",
      "name": "ColabFit Exchange",
    "address": [{
    "@type": "PostalAddress",
    "streetAddress": "736 Broadway",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10003",
    "addressCountry": "US"
  }],
    "keywords": [
      "DDIP",
      "data-driven interatomic potentials",
      "machine learning",
      "materials science",
      "dataset database",
      "data repository",
      "data-driven materials science",
      "data-driven chemistry",
      "data-driven materials discovery",
      "data-driven design",
      "data-driven research",
      "data-driven innovation",
      "data-driven modeling",
      "data-driven simulation",
      "MLIP database",
      "MLIP repository",
      "ab initio",
      "first-principles",
      "density functional theory",
      "molecular dynamics simulations",
      "molecular dynamics trajectories",
      "DFT",
      "machine learning interatomic potentials",
      "MLIP",
      "deep learning interatomic potentials",
      "machine learning potentials"
    ],
    "description": "The ColabFit Exchange is an online resource for the discovery, exploration and submission of datasets for data-driven interatomic potential (DDIP) development for materials science and chemistry applications. ColabFit's goal is to increase the Findability, Accessibility, Interoperability, and Reusability (FAIR) of DDIP data by providing convenient access to well-curated and standardized first-principles and experimental datasets. Content on the ColabFit Exchange is open source and freely available."
  }
  </script>

  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Bootstrap 5 CDN -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container my-5">
'''

count_html = f'''
  <h1 class="mb-4">
    There are {len(cards)} datasets available on <a href="https://colabfit.org" target="_blank">colabfit.org</a>:
  </h1>


</body>
</html>
'''

bottom_html = '''
 </body>
</html>
'''

# Save cleaned HTML
with open('index.html', 'w') as f:
    f.write(top_html + count_html + soup_txt + bottom_html)
