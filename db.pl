process_file(InputFile, OutputFile) :-
    open(InputFile, read, InputStream),    
    open(OutputFile, append, OutputStream),
    
    read_lines(InputStream, OutputStream),
    
    close(OutputStream).

read_lines(InputStream, OutputStream) :-
    repeat,
    read(InputStream, Term),
    (   Term == end_of_file
    ->  !, close(InputStream)
    ;   process_line(Term, OutputStream),
        fail
    ).

process_line(Line, OutputStream) :-
    split_name_and_gender(Line, Name, Gender),    
    make_gender_rule(Name, Gender, OutputStream).

split_name_and_gender(Input, Name, Gender) :-
    atom_chars(Input, Chars),

    append(NameChars, [' ', '(' | Temp], Chars),
    append(GenderChars, [')'], Temp),

    atom_chars(Name, NameChars),
    atom_chars(Gender, GenderChars).

make_gender_rule(Name, Gender, OutputStream) :-
    (
        Gender = 'М',
        atom_concat('male(', Name, Temp),
        atom_concat(Temp, ').', Result),
        write(OutputStream, Result),
        write(OutputStream, '\n')
    );
    (
        Gender = 'Ж',
        atom_concat('female(', Name, Temp),
        atom_concat(Temp, ').', Result),
        write(OutputStream, Result),
        write(OutputStream, '\n')
    ).

    