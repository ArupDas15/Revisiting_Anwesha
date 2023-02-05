import java.io.*;
import java.awt.*;
import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;
import java.util.TreeMap;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;



public class Driver {
    private final String TRIE_DUMP = System.getProperty("user.dir") + "/files/trie_dump.txt";
    private final String LETTER_LIST = System.getProperty("user.dir") + "/files/letter_list.txt";
    private final String BENGALI_FONT = System.getProperty("user.dir") + "/files/bengali_font.ttf";
    private Trie trie;
    private List<String>[] list;
    private TreeMap<String, Integer> tm;
    private boolean[] secondChoice;
    private boolean[] oVowel;
    private String[] oVowelSkip;
    private String[] combination;
    private int top;

    private int loadLetterList(List<String>[] list, TreeMap<String, Integer> tm) throws IOException {
        BufferedReader br = IOHelper.getBufferedReader(LETTER_LIST);

        String buf = br.readLine(); // escaping default new line

        int cnt = 0;
        while((buf = br.readLine()) != null) {
            StringTokenizer tk = new StringTokenizer(buf);
            String eng = tk.nextToken();
            if(!tm.containsKey(eng)) {
                tm.put(eng, cnt);
                list[cnt++] = new ArrayList<>();
            }
            int at = tm.get(eng);
            while(tk.hasMoreTokens()) {
                list[at].add(tk.nextToken());
            }
        }

        int at = tm.get("o");
        list[at].add("");

        br.close();

        return cnt;
    }

    Driver() throws IOException {

        BufferedReader trieReader = IOHelper.getBufferedReader(TRIE_DUMP, (1<<15));

        trie = new Trie(new Bengali(), trieReader);
        list = new List[1024];
        tm = new TreeMap<>();
        secondChoice = new boolean[256];
        oVowel = new boolean[256];
        oVowelSkip = new String[256];
        combination = new String[(1<<18)];

        loadLetterList(list, tm);

        char[] selected = {'`', 'e', 'o', 'i', 'I', 'U', 'u', 'h', 'H', 'g', 'G'};
        for(int i=0; i<selected.length; i++)  secondChoice[selected[i]] = true;

        char[] vowel = {'a', 'e', 'i', 'I', 'o', 'O', 'u', 'U'};
        String[] skip = {"া", "ে", "ি", "ী", "ো", "ো", "ু" , "ূ"};
        for(int i=0; i<vowel.length; i++) {
            oVowel[vowel[i]] = true;
            oVowelSkip[vowel[i]] = skip[i];
        }

        trieReader.close();
    }


    private void produceCombination(String buf, int start, int end, String str) {
        if(start == end) {
            combination[top++] = str;
            return;
        }
        if(start < end-1 && !secondChoice[buf.charAt(start+1)] && str.length() > 0 && !trie.isPrefix(str)) return;
        for(int i=0; i<3; i++)  {
            if(start + i >= end) break;
            String eng = buf.substring(start, start + i + 1);
            if(!tm.containsKey(eng)) continue;
            int at = tm.get(eng);
            for(String ban: list[at]) {
                if(ban.length() == 0 && start+1 < end && oVowel[buf.charAt(start+1)]) {
                    char ch = buf.charAt(start+1);
                    eng = "" + ch;
                    if(!tm.containsKey(eng)) continue;
                    at = tm.get("" + ch);
                    for(String b: list[at]) {
                        if(b.equals(oVowelSkip[ch])) continue;
                        if(str.length() > 0) produceCombination(buf, start + 2, end, str + b);
                    }
                }
                else {
                    if(str.length() + ban.length() > 0) produceCombination(buf, start + i + 1, end, str + ban);
                }
            }
        }
    }

    public String display_values(String str){
        if(str == null || str.length() == 0) return "";
        top = 0;
        produceCombination(str, 0, str.length(), "");
        String[] buf = trie.getSuggestions(combination, top, 12);
        if(buf == null) return "";
        StringBuilder sb = new StringBuilder();
        for(String it: buf) {
            sb.append(it + "\n");
        }
        return sb.toString();

    }
}