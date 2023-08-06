#include <stdio.h>
#define TEST 2

// #define DEBUG (PARSER | DECL_DUMP | TOKENIZER)

#include "makeheaders.c"

// static int MakeCrelmHeaderFile(FILE *header_file, FILE *log_file) {
//   GenState sState;
//   String outStr;
//   IdentTable includeTable;
//   Decl *pDecl;

//   sState.pStr = &outStr;
//   StringInit(&outStr);

//   sState.pTable = &includeTable;
//   memset(&includeTable, 0, sizeof(includeTable));
//   sState.zIf = 0;
//   sState.nErr = 0;
//   sState.zFilename = "(all)";
//   sState.flags = 0;

//   ResetDeclFlags(0);

//   for (pDecl = pDeclFirst; pDecl; pDecl = pDecl->pNext) {
//     DeclareObject(pDecl, &sState, 1);
//   }

//   ChangeIfContext(0, &sState);
//   fprintf(header_file, "%s\n", StringGet(&outStr));

// #ifdef DEBUG
//   fprintf(log_file, "emitting decl: %s\n", StringGet(&outStr));
// #endif

//   IdentTableReset(&includeTable);
//   StringReset(&outStr);
//   return 0;
// }

static int MakeCrelmHeader(char *header, FILE *log_file) {
  GenState sState;
  String outStr;
  IdentTable includeTable;
  Decl *pDecl;

  sState.pStr = &outStr;
  StringInit(&outStr);

  sState.pTable = &includeTable;
  memset(&includeTable, 0, sizeof(includeTable));
  sState.zIf = 0;
  sState.nErr = 0;
  sState.zFilename = "(all)";
  sState.flags = 0;

  ResetDeclFlags(0);

  for (pDecl = pDeclFirst; pDecl; pDecl = pDecl->pNext) {
    DeclareObject(pDecl, &sState, 1);
  }

  ChangeIfContext(0, &sState);
  strcpy(header, StringGet(&outStr));

#ifdef DEBUG
  fprintf(log_file, "emitting decl: '%s'\n", header);
#endif

  IdentTableReset(&includeTable);
  StringReset(&outStr);
  return 0;
}

int make_header(char const *source, char *header) {
  Token *pList;
  FILE *log_file = stdout;
  IdentTable idTable;
  int rv = 0;

#ifdef DEBUG
  debugMask = DEBUG;

  fprintf(log_file, "%s -> %s\n", source, header);
#endif

  memset(&idTable, 0, sizeof(IdentTable));
  pDeclFirst = 0;
  pDeclLast = 0;

#ifdef DEBUG
  printf("%s", source);
#endif

  pList = TokenizeFile(source, &idTable);

  if (!pList) {
    fprintf(log_file, "Errors while processing source\n");
    return 1;
  }

  rv = ParseFile(pList, 0);
  if (!rv) {
    rv = MakeCrelmHeader(header, log_file);
  }

  fflush(log_file);
  FreeTokenList(pList);

  return rv;
}

// int make_header_from_file(char const *source_filename,
//                           char const *header_filename) {
//   Token *pList;
//   FILE *header_file;
//   FILE *log_file = stdout;
//   IdentTable idTable;
//   char *source = 0;
//   int rv = 0;

// #ifdef DEBUG
//   debugMask = DEBUG;

//   fprintf(log_file, "%s -> %s\n", source_filename, header_filename);
// #endif

//   memset(&idTable, 0, sizeof(IdentTable));

//   header_file = fopen(header_filename, "w");
//   if (!header_file) {
//     fprintf(log_file, "Can't create header file '%s'\n", header_filename);
//     return 1;
//   }

//   source = ReadFile(source_filename);
//   if (!source) {
//     fprintf(log_file, "Can't read input file '%s'\n", source_filename);
//     return 1;
//   }

// #ifdef DEBUG
//   printf("%s", source);
// #endif

//   if (0 == strlen(source)) {
//     SafeFree(source);
//     fprintf(log_file, "Input file '%s' is empty.\n", source_filename);
//     return 1;
//   }

// #ifdef DEBUG
//   fprintf(log_file, "Reading %s...\n", source_filename);
// #endif

//   pList = TokenizeFile(source, &idTable);

//   SafeFree(source);

//   if (!pList) {
//     fprintf(log_file, "Errors while processing '%s'\n", source_filename);
//     return 1;
//   }

//   rv = ParseFile(pList, 0);
//   if (!rv) {
//     rv = MakeCrelmHeaderFile(header_file, log_file);
//   }

//   fclose(header_file);
//   fflush(log_file);
//   FreeTokenList(pList);

//   return rv;
// }

// int main(int argc, char *argv[]) {
//   return make_header_from_file(argv[1], argv[2]);
// }