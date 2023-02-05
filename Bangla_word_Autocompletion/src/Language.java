
public interface Language {
    int maxLetter();
    int startLetter();
    int endLetter();
    int mapToInt(int c);
    int retrieveLetter(int v);
    int maxPossibleWordDepth();
    int maxPossibleWordInSuggestion();
    boolean isLetter(int c);
}
