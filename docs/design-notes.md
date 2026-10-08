# Directory design references

The repository was designed after reviewing these public projects. Their structure informed the choices below; their listings, research and prose were not copied into this dataset.

| Reference | Pattern adopted here |
| --- | --- |
| [Public APIs contribution guide](https://github.com/public-apis/public-apis/blob/master/CONTRIBUTING.md) | Consistent record formatting, alphabetical presentation and automated contribution checks |
| [Remote In Tech contribution guide](https://github.com/remoteintech/remote-jobs/blob/main/CONTRIBUTING.md) | Separate files for individual entries, with a consistent contribution process |
| [Awesome Accelerators](https://github.com/ahmadnassri/awesome-accelerators) | A readable Markdown directory as the first browsing surface |
| [Awesome list creation guidance](https://github.com/sindresorhus/awesome/blob/main/create-list.md) | Clear scope, useful curation, contribution guidance and an explicit license |
| [Country Codes dataset](https://github.com/datasets/country-codes) | Downloadable data plus a descriptor and source documentation |
| [Data Package standard](https://datapackage.org/standard/data-package/) | Resource metadata for the CSV, JSON and JSONL exports |

## Choices for this dataset

- **Data first:** the user-provided JSONL contains detailed research, so canonical JSON records retain the complete information rather than collapsing it into a link list.
- **Readable on GitHub:** English and Chinese directory tables link to individual profiles. No application or hosted frontend is required to browse the data.
- **One canonical record per program:** contributors edit small files with stable IDs; build scripts generate all aggregate views and exports.
- **Evidence stays visible:** source links, original-language values, verification dates and the unchanged archive remain accessible.
- **Editorial content is labeled:** supplied scores are retained as editorial opinions and do not dictate the default ordering.
- **Checks have clear limits:** CI catches malformed records and stale exports, while maintainers review source evidence for factual updates.

This project is independently maintained; the references above are not endorsements or affiliations.
