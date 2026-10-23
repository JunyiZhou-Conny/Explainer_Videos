# Review lens 4: spoken flow, TTS, translatability

Script: `videos/ac215-l11-data-labeling-versioning/script.md` at commit 1da63fa, branch
`claude/ac215-l09-l13-batch`.
Method: all 108 SAY blocks were split with `explainer.voice.split_sentences`, which gives 335
sentences. Each sentence went through `KokoroBackend.phonemize`, the call the renderer makes, with the
current `explainer/lexicon.yaml` spliced in. Isolated terms (every row of the script's "Lexicon
candidates" table, plus the numbers and names found in the sweep) were also probed with the raw
`engine.tokenizer.phonemize(…, "en-us")`. Proposed entries were checked by monkeypatching
`load_lexicon` in a throwaway probe. That probe re-phonemized all 335 sentences with and without the
proposed entries: 18 sentences change, all for the better, and no other sentence changes. Every
rewrite marked "verified" was phonemized clean with the entries in place. `lexicon.yaml` was not
edited, and every proposed IPA character is in Kokoro's vocab.

Format: `V<n> · S<scene>.<block>.<sentence> · severity (wrong | confusing | polish) · quote · issue ·
concrete rewrite`.

**Splice trap: clean.** The script's own convention holds. No SAY sentence puts the article "a" or
"A" directly before an existing or proposed lexicon key, so none of them becomes the letter `ˈeɪ`. A
regex sweep with the proposed entries added confirmed this. Both "with a 401" lines (S07.5.3, S15.3.2)
fire the existing guard and come out as `ɐ fˈɔːɹ ˈoʊ wˈʌn`. The one spoken `ˈeɪ` is S04.4.1 "dash a",
where the letter is intended. One related effect to know about: a fragment that ends in "the" before
an entry loses its pre-vowel form ("the implicit dirs flag" gives `ðə ɪmplˈɪsɪt`, not `ðɪ`). That is
harmless, but it is the reason V8 keeps the original word order.

**Homograph sweep: clean except one.** "project" (×10), "console" (×5), "conflict", "rows", "invalid"
and "extract" all get the right stress for their part of speech. "reads" (S15.1.2) and "leads"
(S13.4.4) are present-tense verbs and come out right (`ɹˈiːdz`, `lˈiːdz`). The one miss is the noun
"imports" in S15.2.2 (V21). Watch out when applying fixes: "records" used as a verb comes out as the
noun (`ɹˈɛkɚdz`), so V48 avoids it.

---

## Findings

### wrong

V1 · S12.7.3 · **wrong** · "Then it fingerprinted a manifest, the list of fingerprints and names, and wrote that into the pointer file."
· "that" attaches to the nearest noun phrase, "the list of fingerprints and names", so the ear and a
sentence-aligned Chinese line (把它写入指针文件) both say the manifest itself goes into the pointer
file. The pointer file holds only the manifest's fingerprint (`md5: 89db50de….dir`), and S13 builds
on that distinction ("git keeps the fingerprint of a list of fingerprints"). · "Then it fingerprinted
a manifest, the list of fingerprints and names, and wrote that fingerprint into the pointer file."
(Verified.)

### confusing

V2 · S06.3.2 · confusing · "Put your bucket name on line 23 of docker-shell-CLI.sh, then run it with sh; the ID in the prompt changes every run, and Apple Silicon says aarch64 where this machine says x86."
· (a) Raw `docker-shell-CLI.sh` comes out as `dˈɑːkɚʃˈɛlsˌiːˌɛlˈaɪ.ˌɛsˈeɪtʃ`. The literal "." is a full
stop, so the viewer hears "docker shell C L I. S H". The existing `docker-shell.sh` entry does not
match the longer name. (b) At 32 words with three unrelated clauses, this is a single subtitle cue
holding an edit, a run, and an architecture note. · Add the entry `docker-shell-CLI.sh` (appendix),
and split the sentence: "Put your bucket name on line 23 of docker-shell-CLI.sh, then run it with
sh. The ID in the prompt changes every run, and Apple Silicon says aarch64 where this machine says
x86." (Verified: `dˈɑːkɚ ʃˈɛl sˌiːˌɛlˈaɪ dˈɑːt ˌɛsˈeɪtʃ`.)

V3 · S08.1.2 · confusing · "…then run sh docker-shell-compose.sh."
· The same literal-dot problem: `dˈɑːkɚʃˈɛlkəmpˈoʊz.ˌɛsˈeɪtʃ` ("docker shell compose. S H"). · Add
the entry `docker-shell-compose.sh`. Verified: `ˌɛsˈeɪtʃ dˈɑːkɚ ʃˈɛl kəmpˈoʊz dˈɑːt ˌɛsˈeɪtʃ`.

V4 · S04.7.1, S07.5.3 · confusing · "…a box offering version 1.23.2, because the image tag is latest; this video ran 1.23.0, at the time of recording." / "On Label Studio 1.23.0 it fails with a 401…"
· Raw `1.23.2` comes out as `wˈʌn pɔɪnt tˈuː θɹˈiːpɔɪnt tˈuː` ("one point two three-point two"), and
`1.23.0` the same way. The two version strings differ only in their last digit, and the S04 sentence
contrasts them, so they must be heard cleanly. S04.7.1 is also 29 words. · Add the entries `1.23.0`
and `1.23.2` (house rule: every a.b.c gets one). Split S04.7.1: "Extra checks: the logs show the
server starting, and a box offering version 1.23.2, because the image tag is latest. This video ran
1.23.0, at the time of recording." (Verified: `wˈʌn pɔɪnt twˈɛnti θɹˈiː pɔɪnt tˈuː`.)

V5 · S11.4.2, S15.3.1 · confusing · "…and DVC 3.63.0 is installed, pinned by the lock file." / "…pip gives it a newer DVC, 3.67.1, at the time of recording."
· `θɹˈiː pɔɪnt sˈɪks θɹˈiːpɔɪnt zˈiəɹoʊ` and `θɹˈiː pɔɪnt sˈɪks sˈɛvənpɔɪnt wˈʌn` ("three point six
three-point zero"). S15 contrasts the two versions ("the notebook ran 3.63.0" on the chip), so the
viewer has to hear the difference. · Add the entries `3.63.0` and `3.67.1`. Both sentences were
verified clean.

V6 · S11.1.3, S11.1.4 · confusing · "…package google-cloud-sdk has no installation candidate." / "The message even names the replacement, google-cloud-cli."
· `google-cloud-cli` comes out as `ɡˈuːɡəlklˈaʊdklˈaɪ`, "google cloud CLY", with "cli" read as one
syllable. That is the replacement name the viewer is about to type into the Dockerfile. The `sdk`
form is jammed but audible (`ɡˈuːɡəlklˈaʊdˌɛsdˌiːkˈeɪ`). · Add the entries `google-cloud-cli`
(required) and `google-cloud-sdk` (for a matching rhythm). Verified: `ɡˈuːɡəl klˈaʊd sˌiːˌɛlˈaɪ`.

V7 · S04.8.2 · confusing · "…with the choices brie, gouda, gruyere and parmigiano."
· `gruyere` comes out as `ɡɹˈaɪɚ` ("GRY-er"), which is not the cheese. It is one of the four label
choices the viewer types. · Add the entry `gruyere` = `ɡɹuːjˈɛɹ` ("groo-YAIR"). Verified. See V19
and V20 for the other two cheeses.

V8 · S10.6.2 · confusing · "One flag is not passed, implicit dirs, so gcsfuse only shows folders made in the console: that was the trap."
· "dirs" comes out as `dˈaɪɚz` ("dyers"), so the ear hears "implicit dyers". This flag explains the
whole S10–S12 trap. · Add the multi-word entry `implicit dirs` = `ɪmplˈɪsɪt dˈɜːz` ("implicit durs").
A bare `dirs` key is not needed and would be riskier. Split off the tag-on: "One flag is not passed,
implicit dirs, so gcsfuse only shows folders made in the console. That was the trap." (Verified.)

V9 · S08.1.1 · confusing · "The README's extra runs both containers from one compose file."
· "extra" is a noun here, but the ear parses "extra runs" as an adjective and noun ("additional
runs"). The phonemes even link the two words (`ˈɛkstɹɚ ɹˈʌnz`). · "The README's extra section runs
both containers from one compose file." (Verified.)

V10 · S08.3.3 · confusing · "And the first call is refused: depends on starts Label Studio first, but does not wait until it listens."
· A YAML key used as a bare subject is a garden path: "depends on starts…" makes no sense until the
listener rereads it, and the Chinese line cannot keep it untranslated. · "And the first call is
refused: the depends on setting starts Label Studio first, but does not wait until it listens."
(Verified.)

V11 · S02.6.2 · confusing · "One, pipeline flow, draws this map with a single bucket; no README links it."
· Spoken, "One," sounds like the start of a count ("One: …"), and "pipeline flow" sounds like an
ordinary phrase, not a file name. · "One of them, pipeline flow dot png, draws this map with a single
bucket; no README links it." (Verified.)

V12 · S13.2.2 · confusing · "A gold tag: that is a second copy of the photos, still cents."
· "cents" (`sˈɛnts`) sounds the same as "sense", and "still sense" is a plausible mishearing. The bare
noun with no quantity is also hard to translate. · "A gold tag: that is a second copy of the photos,
still only a few cents." (Verified.)

V13 · S12.10.2 · confusing · "You rename Image 2 to brie 2, and add again."
· This comes out as `ˈɪmɪdʒ tˈuː tə bɹˈiː tˈuː`, "image two to brie two": three /tu/ sounds in a row.
The sentence is a ponder question, so the viewer must parse it on the first hearing. · "You give
Image 2 the new name brie 2, and add again." (Verified.)

V14 · S15 (first SHOW/SAY) · confusing · SHOW: "TRACKER J6, then K5 on "both versions""
· None of S15's SAY lines contains "both versions", so this `wait_until` anchor cannot fire. ·
Rewrite S15.1.1 as two sentences: "Now we fetch both versions, from anywhere. The lecture calls this
time travel: reaching an earlier version, which works only while its files are kept." (Verified,
+4 words.) Alternatively, re-anchor the SHOW on "from anywhere".

V15 · S06.1.2 · confusing · "Your browser hands a cross-origin answer to the page only if it carries a header allowing this origin, and Google adds that header only if the bucket has its own CORS rule."
· At 32 words, this sentence holds the scene's core mechanism with two "only if" conditions chained
together. The ear loses the first condition before the second arrives, and a single Chinese cue would
hold two conditional clauses. · "Your browser hands a cross-origin answer to the page only if it
carries a header that allows this origin. Google adds that header only if the bucket has its own CORS
rule." (Verified.)

V16 · S13.2.3 · confusing · "So the bytes now sit in three places: the images folder you upload to, the cache on your disk where hashing happens, and the DVC store, where every file is named by its fingerprint."
· At 34 words, this is the scene's teaching sentence and recap Q4. The three V6 panels each need an
anchor, and the third sits at word 25. · "So the bytes now sit in three places. The first is the images
folder you upload to. The second is the cache on your disk, where hashing happens. The third is the DVC
store, where every file is named by its fingerprint." (Verified, +8 words.)

V17 · S16.5.1 · confusing · "The whole lecture on one map: Label Studio in a container, signed tickets, a bouncer the bucket configures, labels as small notes, a mounted bucket feeding DVC, photos filed by fingerprint, and a tag pinning the list."
· At 37 words, this is the longest sentence in the script, a verbless list of seven items. "A
bouncer the bucket configures" is a reduced relative clause that both the ear and Chinese word order
struggle with. It also comes close to the forbidden picture, since the bouncer is the browser's and
the bucket only carries the rule. The SHOW relights one piece per item, so each piece needs its own
anchor. · "On one map: Label Studio runs in a container and signs tickets for the photos. A rule on
the bucket satisfies the browser's bouncer. Labels are small notes; a mounted bucket feeds DVC.
Photos are filed by fingerprint; a tag pins the list." (Verified, +6 words. A roomier version opens
with "The whole lecture fits on one map." and uses ", and" in place of the semicolons, but at +12
words it does not fit S16's budget; see the long-sentence section.)

### polish

V18 · S04.5.3, S04.6.2 · polish · "It runs as user 1001…" / "Give the folder to user 1001 with sudo chown…"
· Comes out as "one thousand one". For a user ID, "ten oh one" is what engineers say, and the
script's own candidate table asks for it. · Optional entry `"1001"` = "ten oh one". Verified. No other
video says 1001 in SAY.

V19 · S01.3.4, S04.8.2, S07.1.3, S07.7.2 · polish · "…when someone clicks gouda…"
· Comes out as `ɡˈaʊdə` ("GOW-da"). The script asks the reviewer to pick one reading. The narration is
American (see the Conventions on spelling), and the usual American reading is "GOO-da". · Optional
entry `gouda` = `ɡˈuːdə`. Verified in all 4 lines, with no other sentence affected.

V20 · S04.8.2 · polish · "…and parmigiano."
· `pˌɑːɹmɪdʒiˈɑːnoʊ` ("par-mi-jee-AH-no") has an extra syllable. · Optional entry `parmigiano` =
`pˌɑːɹmɪdʒˈɑːnoʊ` ("par-mi-JAH-no"). Verified.

V21 · S15.2.2 · polish · "Install DVC, run the imports, and sign in with your Google account."
· The noun "imports" gets verb stress (`ɪmpˈɔːɹts`, "im-PORTS"). "the import cell" does the same
(`ɪmpˈɔːɹt sˈɛl`). · "Install DVC, run the cell that imports the libraries, and sign in with your
Google account." (Verified.)

V22 · S04.2.2 · polish · "The flag dash d runs it in the background, the network flag puts it on a private street, and dash p, 8080 colon 8080, publishes the port: a door in your laptop wall."
· At 33 words with three flags, the subtitle cue spans three V1 peel-offs. · "The flag dash d runs it in
the background, and the network flag puts it on a private street. Then dash p, 8080 colon 8080,
publishes the port: a door in your laptop wall." (Verified.)

V23 · S01.3.2 · polish · "In part 2 you will compute this exact string … and it will match the instructor's tag in the class repo, character for character."
· 31 words, and the hook's payoff ("match … character for character") comes at the very end. · "In
part 2 you will compute this exact string on your own laptop from 4 cheese photos. It will match the
instructor's tag in the class repo, character for character." (Verified.)

V24 · S15.1.2 · polish · "The command dvc get, with a tag, walks the rope: it clones the repo at that tag, reads that commit's config to find the bucket, fetches the manifest, then the photos."
· At 31 words, this sentence carries the four V6 rope steps. · "The command dvc get, with a tag, walks
the rope. It clones the repo at that tag, and reads that commit's config to find the bucket. Then it
fetches the manifest, and then the photos." (Verified.)

V25 · S12.2.1 · polish · "The fix is an extra, for Linux: on your laptop, remove the half-made files and mark slash app as a safe directory in your git config, which the container mounts."
· 30 words, two commands in one cue. · "The fix is an extra, for Linux: on your laptop, remove the
half-made files. Then mark slash app as a safe directory in your git config, which the container
mounts." (Verified.)

V26 · S05.1.1 · polish · "Back in the project, open settings, cloud storage, and add source storage with the README's values: Google Cloud Storage, your bucket, the prefix cheeses unlabeled, and pre-signed URLs on."
· 29 words, with a menu path and a value list in one breath. "open settings, cloud storage" also reads
as a list of three actions. · "Back in the project, open settings, then cloud storage, and add source
storage. Use the README's values: Google Cloud Storage, your bucket, the prefix cheeses unlabeled, and
pre-signed URLs on." (Verified.)

V27 · S10.2.1 · polish · "The secrets folder from part 1 already sits beside this repo, and the README wants the same service account and key: reuse both, as an extra tree view shows."
· 29 words. The trailing "as an extra tree view shows" attaches to "reuse both", but it belongs to the
first clause. · "The secrets folder from part 1 already sits beside this repo, as an extra tree view
shows. The README wants the same service account and key, so reuse both." (Verified.)

V28 · S03.1.2 · polish · "In the console, create a service account named data-service-account with the Storage Admin role, then one JSON key, saved in your secrets folder as data-service-account dot json."
· 27 words, and the name comes out jammed (`dˈeɪɾəsˈɜːvɪsɐkˈaʊnt`) twice. · Split the sentence: "In
the console, create a service account named data-service-account, with the Storage Admin role. Then
create one JSON key, and save it in your secrets folder as data-service-account dot json." Optional
spacing entry `data-service-account` (appendix). Verified both ways.

V29 · S13.4.4 · polish · "That is the whole trick: git keeps the fingerprint of a list of fingerprints, and a rope leads from the tag to the bytes in your bucket."
· 27 words, and the V6 rope beat sits at the tail. · "That is the whole trick: git keeps the
fingerprint of a list of fingerprints. A rope leads from the tag to the bytes in your bucket."
(Verified.)

V30 · S12.7.2 · polish · "It fingerprinted each photo with MD5, the values from part 1, and filed each copy under its fingerprint, the first 2 characters naming the shelf."
· 25 words, ending in an absolute construction ("the first 2 characters naming the shelf"). Chinese has
no direct equivalent, and the ear hears "characters" as the subject. · "It fingerprinted each photo with
MD5, the values from part 1. It filed each copy under its fingerprint, on a shelf named by the first 2
characters." (Verified.)

V31 · S12.6.1 · polish · "Our stand-in copies the four photos in, and we add again: now the pointer file says 4 files, 611,101 bytes, and one fingerprint for the folder."
· 26 words. The byte count comes out as "six hundred eleven thousand one hundred one", which is correct
but takes about 2.5 s on its own, inside an already long cue. · "Our stand-in copies the four photos
in, and we add again. Now the pointer file says 4 files, 611,101 bytes, and one fingerprint for the
folder." (Verified.) S14.3.2's "712,574 bytes" is fine because that sentence is short.

V32 · S06.4.1, S09.3.2, S10.7.2, S12.3.1 · polish · four 25-word sentences
· Each one joins two separate ideas, and the Chinese line would carry both. · All four rewrites were
verified.
  - S06.4.1 "This container joins the same street and calls Label Studio by name, not localhost. It
    mounts the repo by its folder name, so keep that name." (This also removes the "so keep that
    name" interjection in the middle.)
  - S09.3.2 "Its SSH command needs your key on GitHub, and this machine has no SSH route. So the same
    branch comes over HTTPS, which the README allows."
  - S10.7.2 "The script also mounts your repo, your secrets and your git config. Set up git before the
    first run, or Docker creates a folder in its place."
  - S12.3.1 "If you cloned main, it stops here: DVC is already set up, and the remote is refused. The
    config still points at the class bucket."

V33 · S02.1.3 · polish · "Labels are the ground truth a model learns from and is graded against, and its labeled mistakes become the next dataset version."
· The second "its" could refer to the labels or to the model, and the Chinese line has to choose. ·
"Labels are the ground truth a model learns from and is graded against. The model's mistakes, once
labeled, go into the next dataset version." (Verified. The anchor "graded against" is kept.)

V34 · S03.5.2 · polish · "An extra count shows 21 images, one a PNG, plus 21 Mac metadata files: upload only the images, or you get 21 broken tasks."
· "one a PNG" is clipped (`wˈʌn ɐ pˌiːˌɛndʒˈiː`), and the sentence has 24 words. · "An extra count shows
21 images, one of them a PNG, plus 21 Mac metadata files. Upload only the images, or you get 21
broken tasks." (Verified.)

V35 · S04.1.2 · polish · "Its script creates the network only if missing, as last lecture, and removes any old container of that name."
· "as last lecture" is not grammatical, and "only if missing" drops its subject. Both get translated
literally. · "Its script creates the network only if it is missing, as in the last lecture, and removes
any old container with that name." (Verified.)

V36 · S04.8.4 · polish · "Underneath, as stand-in calls, the server side: logged in, and project 1 holds the four cheeses."
· The sentence has no main verb until the final clause, so the subtitler has nothing to anchor the
first half to. · "Underneath, our stand-in calls show the server side: we are logged in, and project
1 holds the four cheeses." (Verified.)

V37 · S05.3.4 · polish · "So each cloud step here fails exactly the way a misplaced key fails, the most common mistake in this lecture."
· The trailing appositive could attach to "a misplaced key" or to the failure. L10 had the same
sentence (its V16). · "So each cloud step here fails exactly the way a misplaced key fails. That is the
most common mistake in this lecture." (Verified.)

V38 · S06.5.2 · polish · "…file not found, since ADC looks for the key."
· "since" can be causal or temporal, which is a common Chinese alignment trap. · "…file not found,
because ADC looks for the key." (Verified.)

V39 · S06.6.1 · polish · "With a real key, dash c prints the rule and dash m the bucket settings."
· The second verb is left out, which is hard to follow by ear and does not survive translation. ·
"With a real key, dash c prints the rule, and dash m prints the bucket settings." (Verified.)

V40 · S08.4.1 · polish · "Label Studio keeps running after you leave."
· "leave" what? The capture's `exit` from the command line container is on screen, but the sentence
does not say so. · "Label Studio keeps running after you exit the command line container." (Verified.)

V41 · S09.4.2 · polish · "…as an extra second clone shows; we will see where that bites."
· "bites" is an idiom with no direct Chinese equivalent. · "…we will see where that causes trouble."
(Verified.)

V42 · S09.5.2 · polish · "Its hint mentions master, which is why the branch gets renamed next."
· "Its" could mean the README, the repo or git init. · "Git's hint mentions master, which is why the
branch gets renamed next." (Verified.)

V43 · S09.6.1 · polish · "…with no README, license or gitignore."
· `ɡˈɪɾɪɡnˌɔːɹ` ("GIT-ig-nor") runs the word together. S13.3.3 already says "git ignore file". · "…with
no README, license or git ignore file." (Verified.)

V44 · S10.3.2 · polish · "…the README never says to put the first photos into images, yet later it says to add more."
· Spoken, "into images" sounds generic, not like a folder name. · "…into the images folder, yet later
it says to add more." (Verified.)

V45 · S10.3.3 · polish · "So upload Image 1 to Image 4 from the zip."
· "to" can sound like "two" between two numbered names. · "So upload Image 1 through Image 4 from the
zip." (Verified.)

V46 · S10.7.1 · polish · "…hence privileged and the extra capability."
· A flag name used as a bare adjective sounds like a description, not a flag. · "…hence the
privileged flag and the extra capability." (Verified.)

V47 · S12.5.1 · polish · "…and dvc add happily versions nothing, zero files."
· "versions" as a verb is heard as the plural noun ("happily, versions nothing"). Do not fix it with
"records", which Kokoro reads as the noun. · "…and dvc add happily makes a version with zero files."
(Verified.)

V48 · S14.3.3 · polish · "The class version 21 has a different one, because its fifth photo was another image."
· "one" is two sentences away from its referent. · "The class version 21 has a different manifest
fingerprint, because its fifth photo was another image." (Verified.)

V49 · S15.6.5 · polish · "…left over from an older run; quiet hides errors too."
· A bare flag name used as a subject is heard as the adjective. · "…; the quiet flag hides errors
too." (Verified.)

V50 · S16.4.3 · polish · "Buckets bill until deleted, but never delete the DVC store…"
· "bill" sounds like the name Bill (L10 V10). "until deleted" has no subject. · "Buckets cost money
until you delete them, but never delete the DVC store while any tag should still work; a tag is only a
pointer." (Verified.)

V51 · S07.7.4 · polish · "…a mushroom from an older course app; same shape."
· "same shape" is terse, and it gets translated as a physical shape. · "…; the format is the same."
(Verified.)

V52 · S16.6.3 · polish · "Two: why can the command line container and your browser not swap addresses?"
· The split negation ("can … not") is stiff and delays the point. · "Two: why can't the command line
container and your browser swap addresses?" (Verified: `kˈænt`.)

V53 · S02.6.1, S09.3.4 · polish (series decision) · "…from October 2025…"
· Comes out as "two thousand twenty-five". American speech says "twenty twenty-five". L04 also says
"February 2025" with no entry, so this is a series call, not an L11 defect. · Optional multi-word
entry `October 2025` (appendix). Verified. A bare `"2025"` key would also change L04.

---

## Long sentences (≥ 25 words), status

19 of 335 sentences reach 25 words, and every one has a split above: S16.5.1 37 (V17), S13.2.3 34
(V16), S04.2.2 33 (V22), S06.1.2 32 (V15), S06.3.2 32 (V2), S01.3.2 31 (V23), S15.1.2 31 (V24),
S12.2.1 30 (V25), S04.7.1 29 (V4), S05.1.1 29 (V26), S10.2.1 29 (V27), S03.1.2 27 (V28), S13.4.4 27
(V29), S12.6.1 26 (V31), S12.7.2 25 (V30), and S06.4.1, S09.3.2, S10.7.2, S12.3.1 at 25 (V32). With
all splits applied, the longest remaining sentences are 24 words (S07.2.2, S11.2.1, S13.1.4, S14.4.1), which is acceptable.

Word budget: most rewrites change the count by 0 to 3 words. The large ones are V14 (+4, S15), V16 (+8,
S13) and V17 (+6, S16). S13 (271 against a BRIEF target of 300) and S15 (252 against 250) stay well
inside ±15 %. **S16 is tight.** It is already at 259 against a target of 230, and the cap is 264.
V17 +6, V50 +3 and V52 −1 bring it to 267, so about 3 words must go elsewhere in S16. For example,
"slides only," in S16.3.1 (−2) and "In that order." trimmed to "In order." (−1). The coordinator should
decide, since that wording is a content-lens matter. Re-run `python -m explainer.script` after edits.

## Anchors (SHOW phrases that the SAY must contain)

| SHOW anchor | SAY sentence | status |
| --- | --- | --- |
| S01 "can you get exactly those back" | S01.1.5 | ok, short sentence |
| S02 "graded against" | S02.1.3, word 14 of 22 | ok; kept in V33 |
| S03 "every bucket in the project" | S03.1.3 | ok |
| S05 "tagged recorded" | S05.3.5, words 8–9 | ok |
| S15 "both versions" | **absent** | V14 |
| S04 V1 flag peel-offs (-d, --network, -p) | S04.2.2, words 4–28 of 33 | V22 split puts -p at the start of a sentence |
| S13 V6 three homes | S13.2.3, words 10/15/25 of 34 | V16 split |
| S16 V7 relight, one piece per item | S16.5.1, 7 items in 37 words | V17 split |
| S15 V6 rope steps (clone, config, manifest, blobs) | S15.1.2, words 12–31 | V24 split |

## Translatability notes (no extra findings)

The series metaphors (door, street, phone book, bouncer, ticket, shelf, rope, flag) all match
visuals and render cleanly in Chinese (门, 街道, 电话簿, 门卫, 票, 书架, 绳子, 旗子). Questions are
short and standalone. Condition-at-end clauses ("only if…", "because…") keep English order in
Chinese. Idioms that remain and are acceptable: "pin down", "carry on", "one-off", "sums it up",
"that is the whole trick", "hard refresh". The script avoids "teardown", "read", "live", "content"
and "minute", as its Conventions promise. "Same bouncer as last lecture, now on a bucket" depends
on L10's picture, but the S06 SHOW chip carries that.

---

## Appendix A: lexicon candidates, probed

"Raw" is the isolated `tokenizer.phonemize(w, "en-us")`. "In context" is `KokoroBackend.phonemize` on
the script's own sentence. Cross-video collisions were checked with a whole-word grep over
`videos/*/script.md` SAY lines. None of the proposed keys occurs in another episode's SAY, except
`2025` (L04), which is why V53 uses a multi-word key.

| word | raw Kokoro | verdict | entry |
| --- | --- | --- | --- |
| DVC / dvc | `dˌiːvˌiːsˈiː` (both cases) | ok, no entry | none |
| gcsfuse | `dʒˌiːsˌiːˈɛsfjˈuːz` ("G C S fuse") | ok | none |
| CORS | `kˈɔːɹz` | ok, one syllable | none |
| MD5 | `ˌɛmdˈiː fˈaɪv` | ok | none |
| JSON | `dʒˈeɪsˈɑːn` | ok | none |
| docker-shell-CLI.sh | `dˈɑːkɚʃˈɛlsˌiːˌɛlˈaɪ.ˌɛsˈeɪtʃ` (literal "." pause) | **needs entry** (V2) | yes |
| docker-shell-compose.sh | `dˈɑːkɚʃˈɛlkəmpˈoʊz.ˌɛsˈeɪtʃ` (literal "." pause) | **needs entry** (V3) | yes |
| google-cloud-sdk | `ɡˈuːɡəlklˈaʊdˌɛsdˌiːkˈeɪ` | jammed, entry recommended (V6) | yes |
| google-cloud-cli | `ɡˈuːɡəlklˈaʊdklˈaɪ` ("cly") | **needs entry** (V6) | yes |
| 1.23.0 | `wˈʌn pɔɪnt tˈuː θɹˈiːpɔɪnt zˈiəɹoʊ` | **needs entry** (V4) | yes |
| 1.23.2 | `wˈʌn pɔɪnt tˈuː θɹˈiːpɔɪnt tˈuː` | **needs entry** (V4) | yes |
| 3.63.0 | `θɹˈiː pɔɪnt sˈɪks θɹˈiːpɔɪnt zˈiəɹoʊ` | **needs entry** (V5) | yes |
| 3.67.1 | `θɹˈiː pɔɪnt sˈɪks sˈɛvənpɔɪnt wˈʌn` | **needs entry** (V5) | yes |
| 1.5, 1.76, 3.7 | `wˈʌn pɔɪnt fˈaɪv`, `wˈʌn pɔɪnt sˈɛvən sˈɪks`, `θɹˈiː pɔɪnt sˈɛvən` | ok raw | none |
| 3.8 | existing entry fires: `θɹˈiː pɔɪnt ˈeɪt` | ok | none |
| 1001 | `wˈʌn θˈaʊzənd wˈʌn` | non-idiomatic for a uid, optional (V18) | yes (optional) |
| v20, v21, v25, v30 | `vˈiː twˈɛnti` … `vˈiː θˈɜːɾi` | ok | none |
| aarch64 / x86 | `ˈɑːɹtʃ sˈɪksti fˈɔːɹ` / `ˈɛks ˈeɪɾi sˈɪks` | ok (same as L10) | none |
| sudo | `sˈuːdoʊ` | ok | none |
| chown | `tʃˈaʊn` ("chown", rhymes with town) | ok, a common reading; "C H own" is not needed | none |
| GET | `ɡˈɛt` | ok, not spelled out | none |
| dirs ("implicit dirs") | `dˈaɪɚz` ("dyers") | **needs entry** (V8), multi-word key | yes |
| lakeFS | `lˈeɪk ˌɛfˈɛs` | ok | none |
| gruyere | `ɡɹˈaɪɚ` ("GRY-er") | **needs entry** (V7) | yes |
| parmigiano | `pˌɑːɹmɪdʒiˈɑːnoʊ` | extra syllable, optional (V20) | yes (optional) |
| gouda | `ɡˈaʊdə` ("GOW-da") | acceptable; optional for American "GOO-da" (V19) | yes (optional) |
| amanita | `ˌæmɐnˈiːɾə` ("am-a-NEE-ta") | ok, an accepted reading | none |
| brie | `bɹˈiː` | ok | none |
| E7 | `ˈiː sˈɛvən` | ok | none |
| PNG | `pˌiːˌɛndʒˈiː` | ok | none |
| data-service-account | `dˈeɪɾəsˈɜːvɪsɐkˈaʊnt` (jammed, ×2) | borderline, optional (V28) | yes (optional) |
| October 2025 | `ɑːktˈoʊbɚ tˈuː θˈaʊzənd twˈɛnti fˈaɪv` | series decision (V53) | yes (optional) |
| init (dvc init, git init) | `ɪnɪt` | ok ("in-it") | none |
| gitignore | `ɡˈɪɾɪɡnˌɔːɹ` | run together; fix by rewrite (V43) | none |
| imports (noun) | `ɪmpˈɔːɹts` (verb stress) | fix by rewrite (V21) | none |
| 611,101 / 712,574 | spelled out in full, correct | ok; V31 shortens the cue | none |
| 8080, cli.py, docker-shell.sh, docker-compose.yml, README's, READMEs, ADC, rm, entrypoint, Colab, "a 401" (existing) | all fire correctly | ok | none |
| homophones (not lexicon-fixable) | "cents" = sense (V12), "bill" = Bill (V50), "to" = two (V13, V45) | fix by rewrite | none |

## Appendix B: ready-to-paste lexicon block

Every IPA character below was checked against `engine.tokenizer.vocab`, and every entry was verified
in its script sentence with `load_lexicon` monkeypatched. The required block holds 10 keys, and the
optional block holds 5. Paste it under a new `# AC215 L11` heading. Keys are whole-word and
case-sensitive, and `implicit dirs` and `October 2025` are deliberately multi-word.

```yaml
# AC215 L11 (videos/ac215-l11-data-labeling-versioning); verified against Kokoro af_heart phonemes
"1.23.0": {ipa: "wˈʌn pɔɪnt twˈɛnti θɹˈiː pɔɪnt zˈiəɹoʊ", say: "one point twenty-three point zero"}
"1.23.2": {ipa: "wˈʌn pɔɪnt twˈɛnti θɹˈiː pɔɪnt tˈuː", say: "one point twenty-three point two"}
"3.63.0": {ipa: "θɹˈiː pɔɪnt sˈɪksti θɹˈiː pɔɪnt zˈiəɹoʊ", say: "three point sixty-three point zero"}
"3.67.1": {ipa: "θɹˈiː pɔɪnt sˈɪksti sˈɛvən pɔɪnt wˈʌn", say: "three point sixty-seven point one"}
docker-shell-CLI.sh: {ipa: "dˈɑːkɚ ʃˈɛl sˌiːˌɛlˈaɪ dˈɑːt ˌɛsˈeɪtʃ", say: "docker shell C-L-I dot S-H"}
docker-shell-compose.sh: {ipa: "dˈɑːkɚ ʃˈɛl kəmpˈoʊz dˈɑːt ˌɛsˈeɪtʃ", say: "docker shell compose dot S-H"}
google-cloud-sdk: {ipa: "ɡˈuːɡəl klˈaʊd ˌɛsdˌiːkˈeɪ", say: "google cloud S-D-K"}
google-cloud-cli: {ipa: "ɡˈuːɡəl klˈaʊd sˌiːˌɛlˈaɪ", say: "google cloud C-L-I"}
gruyere: {ipa: "ɡɹuːjˈɛɹ", say: "groo-YAIR"}
implicit dirs: {ipa: "ɪmplˈɪsɪt dˈɜːz", say: "implicit durs"}
# optional (V18, V19, V20, V28, V53)
"1001": {ipa: "tˈɛn ˈoʊ wˈʌn", say: "ten oh one"}
gouda: {ipa: "ɡˈuːdə", say: "GOO-da"}
parmigiano: {ipa: "pˌɑːɹmɪdʒˈɑːnoʊ", say: "par-mi-JAH-no"}
data-service-account: {ipa: "dˈeɪɾə sˈɜːvɪs ɐkˈaʊnt", say: "data service account"}
October 2025: {ipa: "ɑːktˈoʊbɚ twˈɛnti twˈɛnti fˈaɪv", say: "October twenty twenty-five"}
```

---

VERDICT: APPROVE WITH FIXES. 1 wrong (V1, "wrote that into the pointer file" teaches that the
manifest itself goes into the pointer), 16 confusing, 36 polish. The confusing findings include 6
mangled names or numbers that need lexicon entries (two `.sh` names with a literal-dot pause, the
`google-cloud-cli` replacement read "cly", four a.b.c versions, "gruyere", and "implicit dirs" heard
as "dyers"), 1 missing `wait_until` anchor (S15 "both versions"), 3 sentences of 32 words or more on
core mechanisms, and 4 garden paths or homophones. The splice trap is clean: no "a" sits before an
entry, and both "a 401" guards fire. The required lexicon work before TTS is 10 keys (Appendix B),
plus 5 optional ones.
