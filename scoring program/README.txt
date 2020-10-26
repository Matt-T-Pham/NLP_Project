First, be sure to unzip the scoring program file: 
   gzip -d score-answers.pl.gz

To use the scoring program, issue the following command:

   perl score-answers.pl <response_file> <answerkey_file>

For example, you can run the scoring program on the sample files that
are provided to see how it works:

   perl score-answers.pl perfect.response four-stories.answers

   perl score-answers.pl imperfect.response four-stories.answers

-------------------------------------------------------------------
The response_file should contain Question ID and Answer pairs
formatted like so with a blank line between each pair:

      QuestionID: <id>
      Answer: <string>

The answerkey_file should contain an answer key file with entries of
this form, where each entry is separated by a blank line:

      QuestionID: <id>
      Question: <string>
      Answer: <answer strings>
      Difficulty: <string>

===> IMPORTANT: the sequence of QuestionIDs in the response and
answerkey files must be EXACTLY the same! The scoring program will
read both sequences in order and assume that they are aligned. Any
misalignment will cause the scoring program to fail.

-------------------------------------------------------------------
HINT: Given answerkey files for individual stories as we provided, you
can create a single file of answers using the unix "cat" command. For
example: 

       cat *.answers > ALL-answers.txt

will concatenate all of the individual answer key files and save them
in a single file named ALL-answers.txt

Similarly, you can concatenate all of the answers for the story files
that begin with the prefix "2000" using this command: 

       cat 2000*.answers > 2000-answers.txt

The same trick can be used to create a single response file from a set
of individual response files. 
