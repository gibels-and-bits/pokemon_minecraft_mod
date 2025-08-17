package com.example.etbmod.cards;

public class Card {
    private final String id;
    private final String name;
    private final String number;
    private final CardRarity rarity;
    private final String setName;
    private final String imagePath;
    
    public Card(String id, String name, String number, CardRarity rarity, String setName, String imagePath) {
        this.id = id;
        this.name = name;
        this.number = number;
        this.rarity = rarity;
        this.setName = setName;
        this.imagePath = imagePath;
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getNumber() { return number; }
    public CardRarity getRarity() { return rarity; }
    public String getSetName() { return setName; }
    public String getImagePath() { return imagePath; }
}