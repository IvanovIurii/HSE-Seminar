process_file(InputFile, OutputFile) :-
    open(InputFile, read, InputStream),    
    open(OutputFile, append, OutputStream),
    
    read_lines(InputStream, OutputStream),
    
    close(InputStream),
    close(OutputStream).

read_lines(InputStream, OutputStream) :-
    repeat,
    read_line(InputStream, Line),
    (   Line == end_of_file
    ->  !
    ;   (   is_comment(Line) % todo: skip empty lines as well
        -> true
        ;
            (
                write('Line: '),
                write(Line), nl,
                process_line(Line, OutputStream)
            )
        ),
        fail
    ).

is_comment(Line) :-
    sub_atom(Line, 0, 1, _, '#').

read_line(InputStream, Line) :-
    get_char(InputStream, Char),
    (   Char == end_of_file
    ->  Line = end_of_file
    ;   read_line_chars(InputStream, Char, LineChars),
        atom_chars(Line, LineChars)
    ).

read_line_chars(_, '\n', []) :- !. 

read_line_chars(_, end_of_file, []) :- !.

read_line_chars(InputStream, Char, [Char | Rest]) :-
    get_char(InputStream, NextChar),
    read_line_chars(InputStream, NextChar, Rest).

process_line(Line, OutputStream) :-
    (   is_gender_line(Line)
        ->  split_name_and_gender(Line, Name, Gender),    
            make_gender_rule(Name, Gender, OutputStream)
        ; 
        false
    );
    (   is_spouse_line(Line)
        ->  write('Spouse Rule'), nl,
            split_names(Line, Husband, Wife),
            write(Husband), nl,
            make_spouse_rule(Husband, Wife, OutputStream)
        ; 
        false
    ).

is_gender_line(Line) :-
    ( 
        sub_atom(Line, _, 4, _, '(М)')
        ; 
        sub_atom(Line, _, 4, _, '(Ж)') 
    ).

is_spouse_line(Line) :-
    sub_atom(Line, _, _, _, '<->').


split_name_and_gender(Input, Name, Gender) :-
    atom_chars(Input, Chars),

    append(NameChars, [' ', '(' | Temp], Chars),
    append(GenderChars, [')'], Temp),

    atom_chars(Name, NameChars),
    atom_chars(Gender, GenderChars).

split_names(Input, Husband, Wife) :-
    atom_chars(Input, Chars),

    append(NameChars1, [' ', '<', '-', '>', ' ' | Rest], Chars),

    atom_chars(Husband, NameChars1).

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

make_spouse_rule(Husband, Wife, OutputStream) :-
    atom_concat('spouse(', Husband, Temp),
    atom_concat(Temp, ', ', Temp),
    atom_concat(Temp, Wife, Temp),
    atom_concat(Temp, ').', Result),
    write(OutputStream, Result),
    write(OutputStream, '\n').    