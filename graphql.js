const axios = require('axios').default;
const fs = require('fs');
const { request, gql } = require('graphql-request')

async function wikiLookup(namedEntity) {
    const searchString = encodeURI(`${namedEntity}`)
    const data = await axios.get(`https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles=${searchString}&format=json&explaintext=plain`)

    return Object.values(data.data.query.pages)[0]
}

const categories = [
    { name: "environmental", description: "Environmental policy is the commitment of an organization or government to the laws, regulations, and other policy mechanisms concerning environmental issues." },
    { name: "defence", description: "Military policy (also called defence policy or defense policy) is public policy dealing with multinational security and the military. It comprises the measures and initiatives that governments do or do not take in relation to decision-making and strategic goals, such as when and how to commit national armed forces." },
    { name: "education", description: "Consists of the principles and government policies in the educational sphere as well as the collection of laws and rules that govern the operation of education systems. Education occurs in many forms for many purposes through many institutions." },
    { name: "economy", description: "Economic policy is a course of action that is intended to influence or control the behavior of the economy. Economic policies are typically implemented and administered by the government." },
    { name: "legal", description: "Legal policy consists of principles the judges consider the law must uphold, such as: that law should serve the public interest, that it should be fair and just, etc." },
    { name: "social policy", description: "Social policy is policy usually within a governmental or political setting, such as the welfare state and study of social services. Social policy consists of guidelines, principles, legislation and activities that affect the living conditions conducive to human welfare, such as a person's quality of life." },
    { name: "healthcare", description: "Health policy can be defined as the 'decisions, plans, and actions that are undertaken to achieve specific healthcare goals within a society'" },
    {
        name: "indigenous and first nations", description: "Indigenous policy concerns historic and current relationships between Canadians and the distinct societies of First Nations, Inuit, and Métis peoples in Canada. Specifically, building of relationships with Indigenous Peoples that respect their values, ways, and cultures."
    },
    { name: "technology", description: "Technology policy concerns the 'public means for nurturing those capabilities and optimizing their applications in the service of national goals and interests'" },
    { name: "social infrastructure", description: "Social infrastructure refers to facilities and services that help individuals, families, groups, and communities meet their social needs, maximize their potential for development, and enhance community well-being." },
    { name: "transportation", description: "Transport planning deals with the preparation and implementation of actions designed to address specific problems. The goal of transport policy is to make effective decisions concerning the allocation of transport resources, including the management and regulation of existing transportation activities." },
    { name: "agriculture", description: "Agricultural policy describes a set of laws relating to domestic agriculture and imports of foreign agricultural products. Governments usually implement agricultural policies with the goal of achieving a specific outcome in the domestic agricultural product markets." },
    { name: "media", description: "Media policy is a term describing all legislation and political action directed towards regulating the media, especially mass media, and the media industry." },
]

async function parseNamedEntities(f, ne_set, named_entities) {
    const ents = f.named_entities.entities

    for (var i = 0; i < ents.length; i++) {
        const ent = ents[i]
        if (!ne_set.has(ent.word)) {
            console.log(ent.word, ent.entity_group)
            const desc = await wikiLookup(ent.word, ent.entity_group)
            const d = {
                "entity": ent.word,
                "group": ent.entity_group,
                "description": (desc.extract ?? "No good definition found.").split("\n")[0],
            }
            named_entities.push(d)
            ne_set.add(ent.word)
        }
    }
}

async function parseResults(results) {

    const ne_set = new Set()
    const named_entities = []

    for (var i = 0; i < results.length; i++) {
        const f = results[i]
        const obj = JSON.parse(fs.readFileSync(`./results/${f}.json`, 'utf8'));
        await parseNamedEntities(obj, ne_set, named_entities)
    }

    return named_entities
}

// categories
function syncCategories() {
    const reqs = categories.map(category => {
        const query = gql`
        mutation CreateCategory($name: String!, $description: String!) {
            createCategory(data: { title: $name, description: $description }) {
                title
                description
            }
        }
        `

        return request('http://localhost:3000/', query, category)
    })

    Promise.all(reqs).then(console.log)
}
// syncCategories()

// name entities
const results = fs.readdirSync('./results').map(d => d.split(".")[0])
parseResults(results).then(entities => {
    const reqs = entities.map(entity => {
        entity.categories = []
        const query = gql`
        mutation CreateNamedEntity($entity: String!, $group: String!, $description: String!, $categories: [String!]!) {
            createNamedEntity(data: { name: $entity, type: $group, description: $description, categories: $categories }) {
                name
                type
                categories {
                    id
                }
                description
            }
        }
        `

        return request('http://localhost:3000/', query, entity)
    })

    Promise.all(reqs).then(console.log).then(() => {
        // index computation
        console.log('============')
        var ne_set = new Set()
        entities.forEach(ent => ne_set.add(ent.entity))
        ne_set = Array.from(ne_set)
        const longest_entity = Math.max(...(ne_set.map(el => el.length)))

        const cumulative = {}
        for (var i = 0; i < results.length; i++) {
            const f = results[i]
            const obj = JSON.parse(fs.readFileSync(`./results/${f}.json`, 'utf8'));

            const indices = []
            for (var j = 0; j < obj.summary.length - longest_entity; j++) {
                ne_set.forEach(ne => {
                    if (obj.summary.substring(j, j + ne.length) == ne) {
                        indices.push({
                            startPosition: j,
                            endPosition: j + ne.length,
                            entity: ne,
                        })
                    }
                })
            }

            cumulative[f] = indices
        }
        console.log(cumulative)
    })

})