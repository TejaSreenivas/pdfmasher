/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>

#import "HSGUIController.h"
#import "PMPageRepr.h"
#import "PyPageController.h"

@interface PMPageController : HSGUIController
{
    IBOutlet NSView *wholeView;
    IBOutlet NSView *pageReprPlaceholder;
    IBOutlet NSTextField *pageLabelTextField;
    IBOutlet NSButton *reorderModeButton;
    
    PMPageRepr *pageRepr;
}
- (id)initWithPy:(id)aPy;
- (PyPageController *)py;
- (NSView *)view;

- (IBAction)prevPage:(id)sender;
- (IBAction)nextPage:(id)sender;
- (IBAction)toggleShowOrder:(id)sender;
@end