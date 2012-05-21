/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMElementTable.h"

@implementation PMElementTable
- (id)initWithPy:(id)aPy tableView:(PMElementTableView *)aTableView
{
    self = [super initWithPy:aPy view:aTableView];
    columns = [[HSColumns alloc] initWithPy:[[self py] columns] tableView:aTableView];
    [self initializeColumns];
    [self connect];
    return self;
}

- (void)dealloc
{
    [columns release];
    [super dealloc];
}

- (PyElementTable *)py
{
    return (PyElementTable *)py;
}

- (HSColumns *)columns
{
    return columns;
}

- (void)initializeColumns
{
    HSColumnDef defs[] = {
        {@"page", @"Page", 50, 20, 0, YES, nil},
        {@"order", @"Order", 50, 20, 0, YES, nil},
        {@"x", @"X", 50, 20, 0, YES, nil},
        {@"y", @"Y", 50, 20, 0, YES, nil},
        {@"fontsize", @"Font Size", 70, 20, 0, YES, nil},
        {@"text_length", @"Text Length", 70, 20, 0, YES, nil},
        {@"state", @"State", 75, 20, 0, YES, nil},
        {@"text", @"Text", 150, 20, 0, YES, nil},
        nil
    };
    [[self columns] initializeColumns:defs];
    // [[self columns] restoreColumns];
}

/* Delegate */

- (void)flagShortcutPressed:(NSString *)shortcut
{
    [[self py] pressKey:shortcut];
}

@end