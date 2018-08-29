#! /usr/bin/env python3

import sys
import argparse
from subprocess import call

parser = argparse.ArgumentParser(description='Change boldfance for Pandoc Markdown',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('revision',type=str,default="0",
                    help='Git revision to find differences to')
parser.add_argument('blame',type=argparse.FileType('r'),
                    nargs='?',default=sys.stdin,
                    help='Output from git blame -s')
parser.add_argument('out',type=argparse.FileType('w'),
                    nargs='?',default=sys.stdout,
                    help='Output file')
parser.add_argument('--skip-yaml-block',type=bool,default=True,
                    help="Don't circumfix a YAML (when located at top of file)")
parser.add_argument('--prefix',type=str,nargs='?',default='**',
                    help='Prefix changed lines with this symbol')
parser.add_argument('--suffix',type=str,nargs='?',default='**',
                    help='Suffix changed lines with this symbol')

# need to add text about nodiff
# need to add text about being able to work around basic latex formatting
# need to add note that this won't find differences resulting from non-related diffs

def is_ancestor(hashA, hashB):
    '''test whether commit A is an ancestor of commit B'''

    # this is trivial, and we don't allow us to be our own grandpa
    # this won't work if there's a collision in the short hashes, but then again
    # other things would break anyway, so don't be stupid, okay?
    if hashA in hashB or hashB in hashA:
        return False

    # git merge-base returns 0 for ancestor, so we have to negate
    return not call(['git', 'merge-base', '--is-ancestor', hashA, hashB])

yaml_delim = set(['---', '...'])

def main(argv=None):
    args = parser.parse_args(argv)

    lineno = 1

    if args.skip_yaml_block and args.blame.readline().strip() in yaml_delim:
        line = args.blame.readline()

        line = line.split(maxsplit=2)
        rev, gitlineno = line[:2]
        line = line[2] if len(line) == 3 else ''
        rev = rev[1:] if rev[0] == "^" else rev # strip leading caret
        gitlineno = int(gitlineno[:-1]) # strip trailing parenthesis

        print('{}'.format(line.rstrip()),file=args.out)
        # this keeps us form spinning uselessly if we hit the end of a file
        # without ending the header block
        for line in args.blame:
            line = line.split(maxsplit=2)
            rev, gitlineno = line[:2]
            line = line[2] if len(line) == 3 else ''
            rev = rev[1:] if rev[0] == "^" else rev # strip leading caret
            gitlineno = int(gitlineno[:-1]) # strip trailing parenthesis

            lineno += 1
            print('{}'.format(line.rstrip()),file=args.out)
            if line.strip() in yaml_delim:
                break

    #print(lineno,"lines skipped in YAML block")
    in_caption = False
    skip = False
    prefix = args.prefix
    suffix = args.suffix
    for line in args.blame:
        close_env = False

        line = line.split(maxsplit=2)
        rev, gitlineno = line[:2]
        line = line[2] if len(line) == 3 else ''
        rev = rev[1:] if rev[0] == "^" else rev # strip leading caret
        gitlineno = int(gitlineno[:-1]) # strip trailing parenthesis

        line = line.rstrip()
        if "<nodiff>" in line:
            skip = True
        elif "</nodiff>" in line:
            skip = False

        lineno += 1
        #print(int(rev))
        # pandoc assumes everything in a latex block is latex, so we have
        # to do latex style formatting in captions

        if r"\caption{" in line:
            in_caption = True
            if args.prefix in ['*','**']:
                suffix = "}"
                if args.prefix == '*':
                    prefix = r'\emph{'
                else:
                    prefix = r'\textbf{'

        if in_caption and line[-1] == '}':
            in_caption = False
            prefix = args.prefix
            suffix = args.suffix
        if line == ']':
            close_env = True
        begin_capt_lbl = r"\caption{" in line or r"\label{" in line
        empty = len(line) == 0
        header = "#" in line
        modified = is_ancestor(args.revision, rev)

        if modified and not any([header, empty, begin_capt_lbl, skip, close_env]):
            ending = ""
            if line[-2:] == '^[':
                ending = line[-2:]
                line =  line[:-2]
            print('{}{}{}{}'.format(prefix,line,suffix,ending),file=args.out)
        else:
            print('{}'.format(line),file=args.out)


if __name__ == '__main__':
    sys.exit(main())
