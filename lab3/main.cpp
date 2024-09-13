#include <iostream>
#include <string>
#include <vector>
#include <memory>

class Language {
private:
    static const std::string NAME;
    std::string alphabet_type;
    std::string language_family;
    static int object_count;

public:
    Language() : alphabet_type(""), language_family("") {
        object_count++;
    }

    Language(const std::string& alphabet, const std::string& family)
        : alphabet_type(alphabet), language_family(family) {
        object_count++;
    }

    ~Language() {
        object_count--;
        std::cout << "Language object destroyed. Remaining objects: " << object_count << std::endl;
    }

    static std::string getName() { return NAME; }
    std::string getAlphabetType() const { return alphabet_type; }
    std::string getLanguageFamily() const { return language_family; }

    void setAlphabetType(const std::string& alphabet) { alphabet_type = alphabet; }
    void setLanguageFamily(const std::string& family) { language_family = family; }

    static int getObjectCount() { return object_count; }
};

const std::string Language::NAME = "Ukrainian";
int Language::object_count = 0;

class Country {
private:
    std::string name;
    long long population;
    std::string capital;
    std::vector<std::shared_ptr<Language>> official_languages;
    static int object_count;

public:
    Country() : name(""), population(0), capital("") {
        object_count++;
    }

    Country(const std::string& country_name, long long country_population, const std::string& country_capital)
        : name(country_name), population(country_population), capital(country_capital) {
        object_count++;
    }

    ~Country() {
        object_count--;
        std::cout << "Country object destroyed. Remaining objects: " << object_count << std::endl;
    }

    std::string getName() const { return name; }
    long long getPopulation() const { return population; }
    std::string getCapital() const { return capital; }
    const std::vector<std::shared_ptr<Language>>& getOfficialLanguages() const { return official_languages; }

    void setName(const std::string& country_name) { name = country_name; }
    void setPopulation(long long country_population) { population = country_population; }
    void setCapital(const std::string& country_capital) { capital = country_capital; }

    void addOfficialLanguage(std::shared_ptr<Language> lang) {
        official_languages.push_back(lang);
    }

    static int getObjectCount() { return object_count; }
};

int Country::object_count = 0;

int main() {
    auto ukrainian = std::make_shared<Language>("Cyrillic", "Slavic");
    Country ukraine("Ukraine", 35000000, "Kyiv");
    ukraine.addOfficialLanguage(ukrainian);

    std::cout << "Country: " << ukraine.getName() << std::endl;
    std::cout << "Capital: " << ukraine.getCapital() << std::endl;
    std::cout << "Population: " << ukraine.getPopulation() << std::endl;
    std::cout << "Official language: " << Language::getName() << std::endl;
    std::cout << "Language family: " << ukrainian->getLanguageFamily() << std::endl;

    std::cout << "Number of Language objects: " << Language::getObjectCount() << std::endl;
    std::cout << "Number of Country objects: " << Country::getObjectCount() << std::endl;

    return 0;
}
