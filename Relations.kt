package org.example

import java.io.File

// todo: make it DSL
data class Person(
    val name: String,
    val sex: Sex,
    val partners: List<Person> = emptyList(),
    val children: List<Person> = emptyList(),
    val parents: List<Person> = emptyList()
) {
    override fun toString(): String {
        val sb = StringBuilder()
        sb.append("$name (${sex})")

        if (partners.isNotEmpty()) {
            sb.append("\n  Partners:")
            partners.forEach { partner ->
                sb.append("\n    ${partner.name} (${partner.sex})")
            }
        }

        if (children.isNotEmpty()) {
            sb.append("\n  Children: ")
            children.forEach { child ->
                sb.append("\n    ${child.name} (${child.sex})")
            }
        }

        if (parents.isNotEmpty()) {
            sb.append("\n  Parents: ")
            parents.forEach { parent ->
                sb.append("\n    ${parent.name} (${parent.sex})")
            }
        }

        return sb.toString()
    }
}

enum class Sex {
    MALE, FEMALE;

    companion object {
        fun of(sex: String): Sex {
            return when (sex) {
                "М" -> MALE
                "Ж" -> FEMALE
                else -> throw RuntimeException("There is only 2 genders !!!")
            }
        }
    }
}

fun main() {
    val filePath = "input.txt"

    val people = mutableMapOf<String, Sex>()
    val partners = mutableMapOf<String, MutableList<String>>()
    val parentToChild = mutableMapOf<String, MutableList<String>>()
    val childToParent = mutableMapOf<String, MutableList<String>>()

    File(filePath).forEachLine { line ->
        parsePerson(line)?.let { person ->
            people[person.first] = person.second
        }

        
        parsePartners(line)?.let { partnersPair ->
            addToMap(partners, partnersPair.first, partnersPair.second)
            addToMap(partners, partnersPair.second, partnersPair.first)
        }

        parseChild(line)?.let { parentToChildPair ->
            addToMap(parentToChild, parentToChildPair.first, parentToChildPair.second)
            addToMap(childToParent, parentToChildPair.second, parentToChildPair.first)
        }
    }

    val peopleConnected = mutableListOf<Person>()
    for ((name, sex) in people.entries) {
        val personPartners = partners[name]?.mapNotNull { partner ->
            // maybe there is no such person among all the people, then skip
            people[partner]?.let { sex ->
                Person(partner, sex)
            }
        } ?: emptyList()

        val personChildren = parentToChild[name]?.mapNotNull { child ->
            // maybe there is no such person among all the people, then skip
            people[child]?.let { sex ->
                Person(child, sex)
            }
        } ?: emptyList()

        val childrenParents = childToParent[name]?.mapNotNull { parent ->
            // maybe there is no such person among all the people, then skip
            people[parent]?.let { sex ->
                Person(parent, sex)
            }
        } ?: emptyList()

        // if partners.size = 1: 1) either single or 2) child
        peopleConnected.add(
            Person(
                name = name,
                sex = sex,
                partners = personPartners,
                children = personChildren,
                parents = childrenParents
            )
        )
    }

    // todo: add proper test cases
    test(peopleConnected)
}

private fun parsePerson(line: String): Pair<String, Sex>? {
    val nameSexRegex = """(\p{L}+) \(([МЖ])\)""".toRegex()
    val nameSexMatchedResult = nameSexRegex.matchEntire(line) ?: return null

    val name = nameSexMatchedResult.groupValues[1]
    val sex = nameSexMatchedResult.groupValues[2]

    return name to Sex.of(sex)
}

private fun parsePartners(line: String): Pair<String, String>? {
    val maritalStatusRegex = """(\p{L}+) <-> (\p{L}+)""".toRegex()
    val maritalStatusMatchedResult = maritalStatusRegex.matchEntire(line) ?: return null

    val firstPartner = maritalStatusMatchedResult.groupValues[1]
    val secondPartner = maritalStatusMatchedResult.groupValues[2]

    return firstPartner to secondPartner
}

private fun parseChild(line: String): Pair<String, String>? {
    val parentChildRegex = """(\p{L}+) -> (\p{L}+)""".toRegex()
    val nameSexMatchedResult = parentChildRegex.matchEntire(line) ?: return null

    val parent = nameSexMatchedResult.groupValues[1]
    val child = nameSexMatchedResult.groupValues[2]

    return parent to child
}

private fun <K, V> addToMap(map: MutableMap<K, MutableList<V>>, key: K, value: V) {
    if (map.containsKey(key)) {
        map[key]!!.add(value)
    } else {
        map[key] = mutableListOf(value)
    }
}

private fun test(people: List<Person>) {
    search(people, "Петя М") // not found

    search(people, "Платон М") // son of Алексей
    search(people, "Мария Ж") // wife of Bogdan, daughter of Павел
    search(people, "Артемий М") // son of Назар (has multiple kids)

    search(people, "? Игорь")
}

private fun search(people: List<Person>, searchString: String) {
    var found = false
    // todo: split in 2 methods
    var justName = "";
    if (searchString.contains("?")) {
        justName = searchString.replace("? ", "")
    }

    if (justName.isNotEmpty()) {
        people.forEach { person ->
            if (person.name == justName) {
                println("Found by search string '$searchString' person $person")
            }
        }

        return
    }

    // end

    val (name, sex) = searchString.split(" ")
    people.forEach { person ->
        if (person.name == name && person.sex == Sex.of(sex)) {
            println("Found by search string '$searchString' person $person\n")
            found = true

            return@forEach
        }
    }

    if (!found) {
        println("Not found by search string '$searchString'\n")
    }
}

// todo: print male/1, female/1, spouse/2, parent/2 to stdout as logs
// todo: create Person via Kotlin DSL {name, sex}
// todo: create a graph, not a tree
// todo: return error if 2 spouses or mariange between the same sex

// todo: get relations - father / mother / grandfather / grandmother / brother / sister / grandparent
