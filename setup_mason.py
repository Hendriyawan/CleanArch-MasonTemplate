import os
import subprocess

def create_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def main():
    # Initialize mason.yaml configuration
    mason_yaml_path = 'mason.yaml'
    mason_config = '''bricks:
  core_setup:
    path: ./bricks/core_setup
  data_layer:
    path: ./bricks/data_layer
  presentation_layer:
    path: ./bricks/presentation_layer
'''
    create_file(mason_yaml_path, mason_config)

    # =========================================================================
    # BRICK 1: CORE SETUP (Initial Project Template)
    # =========================================================================
    create_file('bricks/core_setup/brick.yaml', '''name: core_setup
description: "Generate Initial App Structure (main, app, injection, core)"
version: 0.1.0+1

vars:
  project_name:
    type: string
    description: "Project Name (e.g., movrev, ingatin)"
    prompt: "Enter Project Name (lowercase, no spaces):"
''')

    core_dir = 'bricks/core_setup/__brick__/lib'

    create_file(f'{core_dir}/main.dart', '''import 'package:flutter/material.dart';
import 'app/app.dart';
import 'app/injection.dart' as di;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Dependency Injection
  await di.init();
  
  runApp(const MyApp());
}
''')

    create_file(f'{core_dir}/app/app.dart', '''import 'package:flutter/material.dart';
import '../core/themes/app_themes.dart';
import '../core/routes/app_routes.dart';
import '../core/config/app_config.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConfig.appName,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      initialRoute: AppRoutes.home,
      onGenerateRoute: AppRoutes.generateRoute,
    );
  }
}
''')

    create_file(f'{core_dir}/app/injection.dart', '''import 'package:get_it/get_it.dart';
import 'package:http/http.dart' as http;

final locator = GetIt.instance;

Future<void> init() async {
  // External
  locator.registerLazySingleton(() => http.Client());

  // Core / Network
  // locator.registerLazySingleton(() => CustomHttpClient(locator()));

  // Features (Data & Domain) will be registered here
}
''')

    create_file(f'{core_dir}/core/config/app_config.dart', '''class AppConfig {
  static const String appName = '{{project_name.titleCase()}}';
  static const String baseUrl = 'https://api.example.com';
  // Add API keys or other configurations here
}
''')

    create_file(f'{core_dir}/core/routes/app_routes.dart', '''import 'package:flutter/material.dart';

class AppRoutes {
  static const String home = '/';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case home:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(child: Text('Home Page')),
          ),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}
''')

    create_file(f'{core_dir}/core/themes/app_themes.dart', '''import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const primary = Color(0xFF00E5FF);
  static const secondary = Color(0xFFFFD700);

  static ThemeData get light => _buildTheme(Brightness.light);
  static ThemeData get dark => _buildTheme(Brightness.dark);

  static ThemeData _buildTheme(Brightness brightness) {
    final isDark = brightness == Brightness.dark;

    final neutral = isDark ? const Color(0xFFFAFAFA) : const Color(0xFF05070A);
    final background = isDark
        ? const Color(0xFF191c1f)
        : const Color(0xFFF5EFE6);
    final surface = isDark ? const Color(0xFF1E1E1E) : const Color(0xFFFBF7F0);
    final inputFill = isDark ? const Color(0xFF2C2C2C) : Colors.white;

    final scheme = ColorScheme.fromSeed(
      seedColor: primary,
      brightness: brightness,
      primary: primary,
      secondary: secondary,
      surface: surface,
    );

    // Helper wrappers
    TextStyle manrope(TextStyle base) => GoogleFonts.manrope(textStyle: base);
    TextStyle plusJakarta(TextStyle base) =>
        GoogleFonts.plusJakartaSans(textStyle: base);

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: background,
      textTheme: TextTheme(
        // ── Display / Headline → Manrope ──────────────────────────────
        displaySmall: manrope(
          TextStyle(
            fontSize: 38,
            height: 1.06,
            fontWeight: FontWeight.w700,
            color: neutral,
          ),
        ),
        headlineMedium: manrope(
          TextStyle(
            fontSize: 24,
            height: 1.15,
            fontWeight: FontWeight.w700,
            color: neutral,
          ),
        ),
        // ── Title → Manrope ───────────────────────────────────────────
        titleLarge: manrope(
          TextStyle(
            fontSize: 20,
            height: 1.2,
            fontWeight: FontWeight.w700,
            color: neutral,
          ),
        ),
        titleMedium: manrope(
          TextStyle(
            fontSize: 16,
            height: 1.25,
            fontWeight: FontWeight.w700,
            color: neutral,
          ),
        ),
        titleSmall: manrope(
          TextStyle(
            fontSize: 14,
            height: 1.3,
            fontWeight: FontWeight.w600,
            color: neutral,
          ),
        ),
        // ── Body → Manrope ────────────────────────────────────────────
        bodyLarge: manrope(
          TextStyle(
            fontSize: 15,
            height: 1.45,
            color: neutral.withValues(alpha: 0.8),
          ),
        ),
        bodyMedium: manrope(
          TextStyle(
            fontSize: 14,
            height: 1.45,
            color: neutral.withValues(alpha: 0.7),
          ),
        ),
        bodySmall: manrope(
          TextStyle(
            fontSize: 12,
            height: 1.4,
            color: neutral.withValues(alpha: 0.6),
          ),
        ),
        // ── Label → Plus Jakarta Sans ─────────────────────────────────
        labelLarge: plusJakarta(
          TextStyle(
            fontSize: 13,
            letterSpacing: 0.4,
            fontWeight: FontWeight.w700,
            color: isDark ? neutral : Colors.white,
          ),
        ),
        labelMedium: plusJakarta(
          TextStyle(
            fontSize: 12,
            letterSpacing: 0.3,
            fontWeight: FontWeight.w600,
            color: neutral.withValues(alpha: 0.8),
          ),
        ),
        labelSmall: plusJakarta(
          TextStyle(
            fontSize: 11,
            letterSpacing: 0.2,
            fontWeight: FontWeight.w500,
            color: neutral.withValues(alpha: 0.6),
          ),
        ),
      ),
      appBarTheme: const AppBarTheme(
        surfaceTintColor: Colors.transparent,
        backgroundColor: Colors.transparent,
        elevation: 0,
        scrolledUnderElevation: 0,
      ),
      navigationBarTheme: NavigationBarThemeData(
        indicatorColor: secondary.withValues(alpha: 0.18),
        backgroundColor: surface,
        surfaceTintColor: Colors.transparent,
        labelTextStyle: WidgetStatePropertyAll(
          GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w700),
        ),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: inputFill,
        selectedColor: secondary.withValues(alpha: 0.18),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(999),
          side: BorderSide(color: neutral.withValues(alpha: 0.08)),
        ),
        labelStyle: GoogleFonts.plusJakartaSans(
          textStyle: TextStyle(color: neutral, fontWeight: FontWeight.w700),
        ),
        side: BorderSide(color: neutral.withValues(alpha: 0.08)),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: inputFill,
        hintStyle: GoogleFonts.manrope(
          textStyle: TextStyle(color: neutral.withValues(alpha: 0.6)),
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(22),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(22),
          borderSide: BorderSide(color: neutral.withValues(alpha: 0.08)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(22),
          borderSide: const BorderSide(color: primary, width: 1.4),
        ),
      ),
      snackBarTheme: SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
        backgroundColor: neutral,
        contentTextStyle: GoogleFonts.manrope(
          textStyle: TextStyle(color: background),
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
      cardTheme: CardThemeData(
        color: surface,
        margin: EdgeInsets.zero,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
      ),
    );
  }
}
''')

    create_file(f'{core_dir}/core/utils/constants.dart', '''class Constants {
  static const String defaultErrorMessage = 'An error occurred. Please try again.';
}
''')

    create_file(f'{core_dir}/core/error/api_exception.dart', '''// ignore_for_file: strict_top_level_inference, prefer_typing_uninitialized_variables

class ApiException {

  final _message;
  ApiException([this._message]);

  @override
  String toString() {
    return "$_message";
  }

}

/// Handle exception during communication
class FetchDataException extends ApiException {
  FetchDataException([String? super.message]);
}

/// Handle exception bad request
class BadRequestException extends ApiException {
  BadRequestException([String? super.message]);
}

/// Handle exception Unauthorized
class UnauthorizedException extends ApiException {
  UnauthorizedException([String? super.message]);
}

/// Handle Exception input
class InvalidInputException extends ApiException {
  InvalidInputException([String? super.message]);
}

/// Handle Exception server
class ErrorException extends ApiException {
  ErrorException([String? super.message]);
}
''')

    create_file(f'{core_dir}/core/error/failure.dart', '''import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  const Failure(this.message);

  @override
  List<Object> get props => [message];
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class ConnectionFailure extends Failure {
  const ConnectionFailure(super.message);
}

class DatabaseFailure extends Failure {
  const DatabaseFailure(super.message);
}
''')

    create_file(f'{core_dir}/core/utils/utils.dart', '''import 'package:flutter/foundation.dart';

void debug(dynamic message) {
  if (kDebugMode) {
    print(message);
  }
}
''')

    create_file(f'{core_dir}/core/network/api_service.dart', '''import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../utils/utils.dart';
import '../error/api_exception.dart';

class ApiService {
  Future getResponse(String url, Map<String, String>? header) async {
    dynamic jsonResponse;
    try {
      final response = await http.get(Uri.parse(url), headers: header);
      jsonResponse = returnResponse(response, url: url);
    } on SocketException {
      throw FetchDataException('No Internet connection');
    }
    return jsonResponse;
  }

  dynamic returnResponse(http.Response response, {String? url = ""}) {
    // Log response for easy debugging
    debug("URL : $url, RESPONSE CODE :${response.statusCode}");
    debug("BODY : ${response.body}");
    debug("HEADER : ${response.headers}");
    debug("");
    debug("");

    // ONLY 200 are considered successful
    if (response.statusCode == 200) {
      var jsonResponse = jsonDecode(response.body.toString());
      return jsonResponse;
    } else {
      // Handle status codes other than 200 (including 401 Unauthorized)
      var res = json.decode(response.body.toString());
      // Retrieve message from API response (adjust key according to your API)
      var message = res['status_message'] ?? res['message'] ?? 'A server error occurred';

      throw FetchDataException(message);
    }
  }
}
''')

    # =========================================================================
    # BRICK 2: DATA LAYER (Data & Domain)
    # =========================================================================
    create_file('bricks/data_layer/brick.yaml', '''name: data_layer
description: "Generate Entity, Model, Repository, and Data Sources"
version: 0.1.0+1

vars:
  entity_name:
    type: string
    description: "Main Entity name (e.g., movie, user, transaction)"
    default: my_entity
    prompt: "Enter Entity name (Data):"
''')

    data_dir = 'bricks/data_layer/__brick__/lib'

    create_file(f'{data_dir}/domain/entities/{{{{entity_name.snakeCase()}}}}.dart', '''import 'package:equatable/equatable.dart';

class {{entity_name.pascalCase()}} extends Equatable {
  final int? id;
  final String? title;

  const {{entity_name.pascalCase()}}({
    this.id,
    this.title,
  });

  @override
  List<Object?> get props => [id, title];
}
''')

    create_file(f'{data_dir}/domain/entities/{{{{entity_name.snakeCase()}}}}_result.dart', '''import '{{entity_name.snakeCase()}}.dart';

class {{entity_name.pascalCase()}}Result {
  final List<{{entity_name.pascalCase()}}> items;
  final int totalPages;

  const {{entity_name.pascalCase()}}Result({
    this.items = const [],
    this.totalPages = 1,
  });
}
''')

    create_file(f'{data_dir}/domain/repositories/{{{{entity_name.snakeCase()}}}}_repository.dart', '''import 'package:fpdart/fpdart.dart';
import '../../../core/error/failure.dart';
import '../entities/{{entity_name.snakeCase()}}_result.dart';
import '../entities/{{entity_name.snakeCase()}}.dart';

abstract class {{entity_name.pascalCase()}}Repository {
  Future<Either<Failure, {{entity_name.pascalCase()}}Result>> get{{entity_name.pascalCase()}}({int page = 1});
  Future<Either<Failure, {{entity_name.pascalCase()}}>> get{{entity_name.pascalCase()}}Detail({required int id});
}
''')

    create_file(f'{data_dir}/data/models/{{{{entity_name.snakeCase()}}}}_model.dart', '''import '../../domain/entities/{{entity_name.snakeCase()}}.dart';

class {{entity_name.pascalCase()}}Model extends {{entity_name.pascalCase()}} {
  const {{entity_name.pascalCase()}}Model({
    super.id,
    super.title,
  });

  factory {{entity_name.pascalCase()}}Model.fromJson(Map<String, dynamic> json) {
    return {{entity_name.pascalCase()}}Model(
      id: json['id'],
      title: json['title'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
    };
  }
}
''')

    create_file(f'{data_dir}/data/datasource/{{{{entity_name.snakeCase()}}}}_remote_data_source.dart', '''import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/{{entity_name.snakeCase()}}_model.dart';

abstract class {{entity_name.pascalCase()}}RemoteDataSource {
  Future<List<{{entity_name.pascalCase()}}Model>> fetch{{entity_name.pascalCase()}}(int page);
}

class {{entity_name.pascalCase()}}RemoteDataSourceImpl implements {{entity_name.pascalCase()}}RemoteDataSource {
  final http.Client client;
  final String baseUrl = 'YOUR_BASE_URL_HERE'; // Replace with API Base URL

  {{entity_name.pascalCase()}}RemoteDataSourceImpl(this.client);

  @override
  Future<List<{{entity_name.pascalCase()}}Model>> fetch{{entity_name.pascalCase()}}(int page) async {
    final response = await client.get(Uri.parse('$baseUrl/{{entity_name.snakeCase()}}?page=$page'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List results = data['results'] ?? [];
      return results.map((e) => {{entity_name.pascalCase()}}Model.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load {{entity_name.titleCase()}}');
    }
  }
}
''')

    create_file(f'{data_dir}/data/datasource/{{{{entity_name.snakeCase()}}}}_local_data_source.dart', '''import 'package:sqflite/sqflite.dart';
import '../models/{{entity_name.snakeCase()}}_model.dart';

abstract class {{entity_name.pascalCase()}}LocalDataSource {
  Future<void> cache{{entity_name.pascalCase()}}(List<{{entity_name.pascalCase()}}Model> items);
  Future<List<{{entity_name.pascalCase()}}Model>> getCached{{entity_name.pascalCase()}}();
}

class {{entity_name.pascalCase()}}LocalDataSourceImpl implements {{entity_name.pascalCase()}}LocalDataSource {
  final Database database;

  {{entity_name.pascalCase()}}LocalDataSourceImpl(this.database);

  @override
  Future<void> cache{{entity_name.pascalCase()}}(List<{{entity_name.pascalCase()}}Model> items) async {
    // Implement database insert here
  }

  @override
  Future<List<{{entity_name.pascalCase()}}Model>> getCached{{entity_name.pascalCase()}}() async {
    // Implement database query here
    return [];
  }
}
''')

    create_file(f'{data_dir}/data/repositories/{{{{entity_name.snakeCase()}}}}_repository_impl.dart', '''import 'package:fpdart/fpdart.dart';
import '../../../core/error/failure.dart';
import '../../../core/error/api_exception.dart';
import '../../domain/entities/{{entity_name.snakeCase()}}_result.dart';
import '../../domain/entities/{{entity_name.snakeCase()}}.dart';
import '../../domain/repositories/{{entity_name.snakeCase()}}_repository.dart';
import '../datasource/{{entity_name.snakeCase()}}_remote_data_source.dart';
import '../datasource/{{entity_name.snakeCase()}}_local_data_source.dart';

class {{entity_name.pascalCase()}}RepositoryImpl implements {{entity_name.pascalCase()}}Repository {
  final {{entity_name.pascalCase()}}RemoteDataSource remoteDataSource;
  final {{entity_name.pascalCase()}}LocalDataSource localDataSource;

  {{entity_name.pascalCase()}}RepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, {{entity_name.pascalCase()}}Result>> get{{entity_name.pascalCase()}}({int page = 1}) async {
    try {
      final models = await remoteDataSource.fetch{{entity_name.pascalCase()}}(page);
      return Right({{entity_name.pascalCase()}}Result(
        items: models,
      ));
    } on FetchDataException catch (e) {
      return Left(ServerFailure(e.message ?? 'Server error occurred'));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, {{entity_name.pascalCase()}}>> get{{entity_name.pascalCase()}}Detail({required int id}) async {
    return Left(const ServerFailure('UnimplementedError'));
  }
}
''')

    # =========================================================================
    # BRICK 3: PRESENTATION LAYER (UI + Usecase)
    # =========================================================================
    create_file('bricks/presentation_layer/brick.yaml', '''name: presentation_layer
description: "Generate Feature UI (BLoC, Page) and its UseCase"
version: 0.1.0+1

vars:
  feature_name:
    type: string
    description: "Feature/Page Name (e.g., now playing, search movie)"
    prompt: "Enter Feature UI Name:"
  entity_name:
    type: string
    description: "Entity Name from Data Layer used (e.g., movie, user)"
    prompt: "Enter Entity Repository Name used:"
''')

    pres_dir = 'bricks/presentation_layer/__brick__/lib'

    create_file(f'{pres_dir}/domain/usecases/get_{{{{feature_name.snakeCase()}}}}_use_case.dart', '''import 'package:fpdart/fpdart.dart';
import '../../../core/error/failure.dart';
import '../entities/{{entity_name.snakeCase()}}_result.dart';
import '../repositories/{{entity_name.snakeCase()}}_repository.dart';

class Get{{feature_name.pascalCase()}}UseCase {
  final {{entity_name.pascalCase()}}Repository _repository;

  Get{{feature_name.pascalCase()}}UseCase(this._repository);

  Future<Either<Failure, {{entity_name.pascalCase()}}Result>> call({int page = 1}) async {
    return await _repository.get{{entity_name.pascalCase()}}(page: page);
  }
}
''')

    create_file(f'{pres_dir}/presentation/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.snakeCase()}}}}_event.dart', '''import 'package:equatable/equatable.dart';

abstract class {{feature_name.pascalCase()}}Event extends Equatable {
  const {{feature_name.pascalCase()}}Event();

  @override
  List<Object?> get props => [];
}

class {{feature_name.pascalCase()}}Initial extends {{feature_name.pascalCase()}}Event {}

class {{feature_name.pascalCase()}}LoadMore extends {{feature_name.pascalCase()}}Event {}
''')

    create_file(f'{pres_dir}/presentation/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.snakeCase()}}}}_state.dart', '''import 'package:equatable/equatable.dart';
import '../../domain/entities/{{entity_name.snakeCase()}}.dart';

class {{feature_name.pascalCase()}}State extends Equatable {
  final bool isLoading;
  final bool isLoadingMore;
  final bool hasMore;
  final List<{{entity_name.pascalCase()}}> items;
  final String? errorMessage;

  const {{feature_name.pascalCase()}}State({
    this.isLoading = false,
    this.isLoadingMore = false,
    this.hasMore = true,
    this.items = const <{{entity_name.pascalCase()}}>[],
    this.errorMessage,
  });

  {{feature_name.pascalCase()}}State copyWith({
    bool? isLoading,
    bool? isLoadingMore,
    bool? hasMore,
    List<{{entity_name.pascalCase()}}>? items,
    String? errorMessage,
  }) {
    return {{feature_name.pascalCase()}}State(
      isLoading: isLoading ?? this.isLoading,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
      hasMore: hasMore ?? this.hasMore,
      items: items ?? this.items,
      errorMessage: errorMessage,
    );
  }

  @override
  List<Object?> get props => [
        isLoading,
        isLoadingMore,
        hasMore,
        items,
        errorMessage,
      ];
}
''')

    create_file(f'{pres_dir}/presentation/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.snakeCase()}}}}_bloc.dart', '''import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/entities/{{entity_name.snakeCase()}}.dart';
import '../../domain/usecases/get_{{feature_name.snakeCase()}}_use_case.dart';
import '{{feature_name.snakeCase()}}_event.dart';
import '{{feature_name.snakeCase()}}_state.dart';

class {{feature_name.pascalCase()}}Bloc extends Bloc<{{feature_name.pascalCase()}}Event, {{feature_name.pascalCase()}}State> {
  final Get{{feature_name.pascalCase()}}UseCase _useCase;
  int _page = 1;

  {{feature_name.pascalCase()}}Bloc(this._useCase) : super(const {{feature_name.pascalCase()}}State()) {
    on<{{feature_name.pascalCase()}}Initial>((event, emit) => _fetchInitial(emit));
    on<{{feature_name.pascalCase()}}LoadMore>(_onLoadMore);
  }

  Future<void> _fetchInitial(Emitter<{{feature_name.pascalCase()}}State> emit) async {
    _page = 1;
    emit(state.copyWith(
      isLoading: true,
      isLoadingMore: false,
      hasMore: true,
      items: const <{{entity_name.pascalCase()}}>[],
    ));

    final result = await _useCase(page: _page);
    
    result.fold(
      (failure) {
        emit(state.copyWith(isLoading: false, hasMore: false, errorMessage: failure.message));
      },
      (data) {
        emit(state.copyWith(
          isLoading: false,
          items: data.items,
          hasMore: _page < data.totalPages,
        ));
      },
    );
  }

  Future<void> _onLoadMore({{feature_name.pascalCase()}}LoadMore event, Emitter<{{feature_name.pascalCase()}}State> emit) async {
    if (state.isLoading || state.isLoadingMore || !state.hasMore) return;
    
    emit(state.copyWith(isLoadingMore: true));
    
    final nextPage = _page + 1;
    final result = await _useCase(page: nextPage);
    
    result.fold(
      (failure) {
        emit(state.copyWith(isLoadingMore: false, errorMessage: failure.message));
      },
      (data) {
        _page = nextPage;
        emit(state.copyWith(
          isLoadingMore: false,
          items: [...state.items, ...data.items],
          hasMore: _page < data.totalPages,
        ));
      },
    );
  }
}
''')

    create_file(f'{pres_dir}/presentation/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.snakeCase()}}}}_page.dart', '''import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '{{feature_name.snakeCase()}}_bloc.dart';
import '{{feature_name.snakeCase()}}_state.dart';

class {{feature_name.pascalCase()}}Page extends StatelessWidget {
  const {{feature_name.pascalCase()}}Page({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('{{feature_name.titleCase()}}'),
      ),
      body: BlocBuilder<{{feature_name.pascalCase()}}Bloc, {{feature_name.pascalCase()}}State>(
        builder: (context, state) {
          if (state.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state.errorMessage != null) {
            return Center(child: Text(state.errorMessage!));
          }
          if (state.items.isEmpty) {
            return const Center(child: Text('No data available.'));
          }

          return ListView.builder(
            itemCount: state.items.length + (state.hasMore ? 1 : 0),
            itemBuilder: (context, index) {
              if (index >= state.items.length) {
                return const Center(child: CircularProgressIndicator());
              }
              final item = state.items[index];
              return ListTile(title: Text(item.title ?? 'Unknown'));
            },
          );
        },
      ),
    );
  }
}
''')

    print("Mason bricks generated successfully!")

if __name__ == '__main__':
    main()
