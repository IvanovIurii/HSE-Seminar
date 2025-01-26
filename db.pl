parse_input_file(InputFile, OutputFile) :-
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
    ;   write(Line), nl,
        process_line(Line, OutputStream),
        fail
    ).

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
        is_spouse_line(Line)
        ->  split_names(Line, Husband, Wife, ' <-> '),
            make_spouse_rule(Husband, Wife, OutputStream) 
        ;
        is_parent_child_line(Line)
        ->  split_names(Line, Parent, Child, ' -> '),
            make_parent_child_rule(Parent, Child, OutputStream)
    ).

is_gender_line(Line) :-
    sub_atom(Line, _, _, _, '(М)');
    sub_atom(Line, _, _, _, '(Ж)').

is_spouse_line(Line) :-
    sub_atom(Line, _, _, _, '<->').

is_parent_child_line(Line) :-
    sub_atom(Line, _, _, _, '->').

split_name_and_gender(Input, Name, Gender) :-
    atom_chars(Input, Chars),

    append(NameChars, [' ', '(' | Temp], Chars),
    append(GenderChars, [')'], Temp),

    atom_chars(Name, NameChars),
    atom_chars(Gender, GenderChars).

split_names(Input, Husband, Wife, Delimiter) :-
    atom_chars(Input, Chars),
    atom_chars(Delimiter, DelimiterChars),

    append(NameChars1, DelimiterCharsAndRest, Chars),
    append(DelimiterChars, Rest, DelimiterCharsAndRest),
    
    atom_chars(Husband, NameChars1),
    atom_chars(Wife, Rest).

make_gender_rule(Name, Gender, OutputStream) :-
    (
        Gender = 'М',
        atom_concat('male(\'', Name, Temp),
        atom_concat(Temp, '\').', Result),
        write(OutputStream, Result),
        write(OutputStream, '\n')
    );
    (
        Gender = 'Ж',
        atom_concat('female(\'', Name, Temp),
        atom_concat(Temp, '\').', Result),
        write(OutputStream, Result),
        write(OutputStream, '\n')
    ).

make_spouse_rule(Husband, Wife, OutputStream) :-
    atom_concat('spouse(\'', Husband, Temp1),
    atom_concat(Temp1, '\', \'', Temp2),
    atom_concat(Temp2, Wife, Temp3),
    atom_concat(Temp3, '\').', Result),

    write(OutputStream, Result),
    write(OutputStream, '\n').    

make_parent_child_rule(Parent, Child, OutputStream) :-
    atom_concat('parent(\'', Parent, Temp1),
    atom_concat(Temp1, '\', \'', Temp2),
    atom_concat(Temp2, Child, Temp3),
    atom_concat(Temp3, '\').', Result),

    write(OutputStream, Result),
    write(OutputStream, '\n').   